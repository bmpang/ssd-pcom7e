from datetime import datetime
from getpass import getpass
from sqlite3 import IntegrityError

import pwinput

from data_access.app_dao import *
from model.artifact import Artifact
from model.copyrightable_material import (
    CopyrightableMaterial,
    FileSizeTooLargeException,
    InvalidCopyrightableMaterialTypeException,
)
from util.checksum_util import generate_checksum_from_bytes
from util.encryption_util import create_salt, decrypt, hash_data
from util.otp_util import send_otp_to_email
from util.pw_validator import validatePassword


# This function creates a session object and determines the user's identity and role which will inform the app what options to present to the user
# In order to establish identity, it will either process a log on action or prompt a new user to register
def initiate_session(sess):
    sess.user_email = input("Email: ").lower()
    if is_email_registered(sess.user_email):
        log_on(sess)
    else:
        register(sess)
    return


# This function verifies a user's account is unlocked and that they have the correct password before initializing the session
# The lock functionality prevents someone from accessing another user's account if they dont know the password.
def log_on(sess):
    # The only remediative action for a user that is locked out is for an administrator to unlock their account for them
    if is_locked(sess.user_email):
        print(
            "Your user account is currently locked - please reach out the system administrator to unlock your account"
        )
    else:
        # All users have a randomly generated salt that is used to uniquely obfuscate each password in the database
        salt = get_salt(sess.user_email)
        attempt = 1
        while attempt < 4:
            # Passwords are immediately salted and hashed so that plaintext is never in memory.
            salted_and_hashed_password = hash_data(
                pwinput.pwinput(prompt="Password: ", mask="*"), salt
            )

            # If the salted and hashed passcode matches the stored value, a user will be logged on and the session is finalized
            if user_auth(sess.user_email, salted_and_hashed_password):
                print("User logged in successfully")
                input("Press any key to continue...")
                sess.user_id = get_user_id(sess.user_email)
                sess.role = get_role(sess.user_email)
                sess.user_name = get_user_name(sess.user_email)
                break
            else:
                print("Password incorrect - please try again!")
                attempt = attempt + 1

                # After three failed attempts, accounts are locked. The admin account cannot be locked.
                if attempt == 4 and sess.user_email != "admin@trackmanagement.com":
                    lock_user(sess.user_email)
                    print(
                        "Your user account has been locked - please reach out the system administrator to unlock your account"
                    )
    return


# this method shows summaries for all copyrightable materials by all artists currently managed in the system
def view_all_artifacts():
    artifact_summaries = []

    # Print a message instead of a blank line if there are no artifacts
    if get_artifact_summaries() == None:
        print("No Artifacts Found")
    else:
        for summary_list in get_artifact_summaries():
            artifact_summaries.append(
                summary_list[2] + " for " + summary_list[1] + " by " + summary_list[0]
            )
        for artifact in artifact_summaries:
            print(artifact)


# this method creates a new artifact of an inputted material type and serializes an encrypted copy of it to our database
def create_artifact(artist_id):
    title = input(
        "What is the title of the work you are uploading copyrightable material for? "
    )
    copyrightable_material_type = input(
        "What type of copyrightable material would you like to add - AUDIO, LYRICS, or SCORE? "
    )

    # A material type for a song should only have one active file at a time
    if artifact_exists(artist_id, title, copyrightable_material_type):
        print(
            "You already have an artifact for that copyrightable material. Please use the modify action to upload a new file."
        )
        return

    file_path = input("Please input the filepath for your copyrightable material ")

    try:
        copyrightable_material = CopyrightableMaterial(
            artist_id, title, file_path, copyrightable_material_type.upper()
        )

    # If there is no file at the path inputted, there is nothing to upload
    except FileNotFoundError:
        print("No file was found at the path you have provided")
        return

    # Files that are too large are not allowed
    except FileSizeTooLargeException:
        print("The file you have pathed too is too large.")
        return

    # the artifact must be of type audio, lyrics, or score
    except InvalidCopyrightableMaterialTypeException:
        print("Please pick a material type of AUDIO, LYRICS, or SCORE")
        return

    artifact = Artifact(copyrightable_material)

    try:
        create_artifact_row(artifact)
        time = datetime.now()
    # if there is a checksum collision, then the supplied file is already managed elsewhere in the database
    except IntegrityError:
        print(
            "That file is already being managed as copyrightable material. Please check your path and try again."
        )
        return

    artifact_id = get_artifact_id(artist_id, title, copyrightable_material_type)

    # create a new timestamp record in the audit log
    create_artifact_audit_log(artist_id, artifact_id, "Created", time)

    print("Successfully created an artifact for your copyrightable material")


# This method retrieves summaries of copyrightable material belonging to a single artist
def view_artists_artifacts(artist_id):
    artifact_summaries = []

    for summary_list in get_artists_artifact_summaries(artist_id):
        artifact_summaries.append(summary_list[1] + " for " + summary_list[0])

    for artifact in artifact_summaries:
        print(artifact)


# this method retrieves the encrypted copy of an existing artifact and saves it to an unencrypted local file
def download_from_artifact(artist_id):
    title = input("Which song would you like to download? ")
    print("What type of copyrightable material would you like to download for " + title)

    copyrightable_material_type = input("AUDIO, LYRICS, or SCORE ").upper()

    artifact_id = get_artifact_id(artist_id, title, copyrightable_material_type)

    # if there is no matching record for the given song and material type, there is nothing to download
    if not artifact_id:
        print(
            "We could not find a "
            + copyrightable_material_type
            + " artifact for "
            + title
        )
        print("Please check your spelling and try again")
        return

    file_info = get_file_info_from_artifact(
        artist_id, title, copyrightable_material_type
    )
    time = datetime.now()

    # create a timestamp record for the download
    create_artifact_audit_log(artist_id, artifact_id, "Downloaded", time)

    file_name = file_info[0] + "_" + file_info[1] + file_info[2]
    file_data = decrypt(file_info[3])

    # If the checksum stored in the database does not match the checksum for the decrypted data, there is a mismatch
    # with what was retrieved and what was expected which means there is a data problem.
    local_checksum = generate_checksum_from_bytes(file_data)
    stored_checksum = get_checksum(artist_id, title, copyrightable_material_type)
    if local_checksum != stored_checksum:
        print("Checksum error. Please contact an administrator")
        return

    with open(file_name, "wb") as new_file:
        new_file.write(file_data)

    print("Copyrightable material was successfully downloaded to the working directory")


# This method allows an artist to upload a new file/version of an existing material
def modify_artifact(artist_id):
    title = input("Which song would you like to upload a new version for? ")
    print("What type of copyrightable material would you like to upload for " + title)
    copyrightable_material_type = input("AUDIO, LYRICS, or SCORE ").upper()

    # if there is no matching record for the given song and material type, there is nothing to modify
    if not artifact_exists(artist_id, title, copyrightable_material_type):
        print(
            "We could not find a "
            + copyrightable_material_type
            + " artifact for "
            + title
        )
        print("Please check your spelling and try again")
        return

    file_path = input("Please input the filepath for your copyrightable material ")

    try:
        copyrightable_material = CopyrightableMaterial(
            artist_id, title, file_path, copyrightable_material_type.upper()
        )

    # If there is no file at the path inputted, there is nothing to upload
    except FileNotFoundError:
        print("No file was found at the path you have provided")
        return

    # Files that are too large are not allowed
    except FileSizeTooLargeException:
        print("The file you have pathed too is too large.")

    # the artifact must be of type audio, lyrics, or score
    except InvalidCopyrightableMaterialTypeException:
        print("Please pick a material type of AUDIO, LYRICS, or SCORE")

    artifact = Artifact(copyrightable_material)

    try:
        update_artifact(artifact)
        time = datetime.now()

    # if there is a checksum collision, then the supplied file is already managed elsewhere in the database
    except IntegrityError:
        print(
            "That file is already being managed as copyrightable material. Please check your path and try again."
        )
        return

    artifact_id = get_artifact_id(artist_id, title, copyrightable_material_type)

    # create a time stamp record for the modification
    create_artifact_audit_log(artist_id, artifact_id, "Modified", time)

    print("Successfully modified artifact")


# This function allows a user to delete an artifact
def delete_artifact(artist_id):
    title = input("Which song would you like to remove an artifact for? ")
    print("What type of copyrightable material would you like to delete for " + title)
    copyrightable_material_type = input("AUDIO, LYRICS, or SCORE ").upper()

    # if there is no matching record for the given song and material type, there is nothing to delete
    if not artifact_exists(artist_id, title, copyrightable_material_type):
        print(
            "We could not find a "
            + copyrightable_material_type
            + " artifact for "
            + title
        )
        print("Please check your spelling and try again")
        return

    delete_artifact_row(artist_id, title, copyrightable_material_type)
    print("Successfully deleted row")


# This function unlocks a user account which was locked after 3 incorrect provided password
def unlock_user(user_id):
    unlock_user_ID(user_id)
    return


# This funtion registers a new user and adds them to the database table users
def register(sess):
    # Using the OTP verification ensures a new user is using their own email
    print("Sending you a one time passcode")
    otp_code = send_otp_to_email(sess.user_email)

    failures = 0

    # If the user cannot verify, then they are likely trying to use an email they do not own and registration ends
    while failures < 3:
        input_otp = input("OTP Code: ")

        if input_otp == otp_code:
            break

        print("OTP Code incorrect, please try again")
        failures += 1

    if failures == 3:
        print("Your email could not be verified, please try registering again later.")
        return

    # Create a new random salt that will be used for uniquely obfuscating the user's password
    salt = create_salt()

    user_pw = pwinput.pwinput(prompt="Enter password: ", mask="*")
    while validatePassword(user_pw) == False:
        print(
            "Invalid password: your password needs to have at least 8 characters, one being uppercase, one being a digit and one being a special character"
        )
        user_pw = pwinput.pwinput(prompt="Enter password: ", mask="*")

    # Immediately salt and hash the password so that the credential is never stored in memory, for privacy and security
    salted_and_hashed_password = hash_data(user_pw, salt)

    first_name = input("Enter first name: ")
    surname = input("Enter last name: ")
    acct_status = "active"
    sess.role = "ARTIST"

    print("Welcome new Artist")

    # Persist the new user to the database
    addUser(
        first_name,
        surname,
        sess.user_email,
        salted_and_hashed_password,
        "ARTIST",
        acct_status,
        salt,
    )

    # Redirect the newly registered user to log on
    log_on(sess)
