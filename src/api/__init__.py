import os
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


# This function will either logon or register a user and initialize the app to be aware of the user's role and identity
def initiate_session(sess):
    sess.user_email = input("Email: ")
    if is_email_registered(sess.user_email):
        log_on(sess)
    else:
        register(sess)
    return


# This function verifies a user's account is unlocked and that they have the correct password before initializing the session
def log_on(sess):
    if is_locked(sess.user_email):
        print(
            "Your user account is currently locked - please reach out the system administrator to unlock your account"
        )
    else:
        salt = get_salt(sess.user_email)
        attempt = 1
        while attempt < 4:

            # salted_and_hashed_password = hash_data(input("Enter password: "), salt)
            salted_and_hashed_password = hash_data(
                pwinput.pwinput(prompt="Password: ", mask="*"), salt
            )

            if user_auth(sess.user_email, salted_and_hashed_password):
                print("User logged in successfully")
                sess.user_id = get_user_id(sess.user_email)
                sess.role = get_role(sess.user_email)
                break
            else:
                print("Password incorrect - please try again!")
                attempt = attempt + 1
                if attempt == 4:
                    lock_user(sess.user_email)
                    print(
                        "Your user account has been locked - please reach out the system administrator to unlock your account"
                    )
    return


# this method shows summaries for all copyrightable materials by all artists currently managed in the system
def view_all_artifacts():
    artifact_summaries = []
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
    except FileNotFoundError:
        print("No file was found at the path you have provided")
        return
    except FileSizeTooLargeException:
        print("The file you have pathed too is too large.")
        return
    except InvalidCopyrightableMaterialTypeException:
        print("Please pick a material type of AUDIO, LYRICS, or SCORE")
        return

    artifact = Artifact(copyrightable_material)

    try:
        create_artifact_row(artifact)
        time = datetime.now()
    except IntegrityError:
        print(
            "That file is already being managed as copyrightable material. Please check your path and try again."
        )
        return

    artifact_id = get_artifact_id(artist_id, title, copyrightable_material_type)
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

    create_artifact_audit_log(artist_id, artifact_id, "Downloaded", time)

    file_name = file_info[0] + "_" + file_info[1] + file_info[2]
    file_data = decrypt(file_info[3])

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
    except FileSizeTooLargeException:
        print("The file you have pathed too is too large.")
    except InvalidCopyrightableMaterialTypeException:
        print("Please pick a material type of AUDIO, LYRICS, or SCORE")

    artifact = Artifact(copyrightable_material)

    try:
        update_artifact(artifact)
        time = datetime.now()
    except IntegrityError:
        print(
            "That file is already being managed as copyrightable material. Please check your path and try again."
        )
        return

    artifact_id = get_artifact_id(artist_id, title, copyrightable_material_type)
    create_artifact_audit_log(artist_id, artifact_id, "Modified", time)

    print("Successfully modified artifact")


# This function allows an Artist to delete their artifact or the ADMIN to delete any artifact


def delete_artifact(artist_id):
    title = input("Which song would you like to remove an artifact for? ")
    print("What type of copyrightable material would you like to delete for " + title)
    copyrightable_material_type = input("AUDIO, LYRICS, or SCORE ").upper()

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
    print("Sending you a one time passcode")
    otp_code = send_otp_to_email(sess.user_email)

    failures = 0

    while failures < 3:
        input_otp = input("OTP Code: ")

        if input_otp == otp_code:
            break

        print("OTP Code incorrect, please try again")
        failures += 1

    if failures == 3:
        print("Your email could not be verified, please try registering again later.")
        return

    salt = create_salt()
    # Immediately salt and hash the password so that the credential is never stored in memory, for privacy and security
    salted_and_hashed_password = hash_data(
        pwinput.pwinput(prompt="Enter password: ", mask="*"), salt
    )
    first_name = input("Enter first name: ")
    surname = input("Enter last name: ")
    acct_status = "active"

    sess.role = "ARTIST"

    print("Welcome new Artist")
    addUser(
        first_name,
        surname,
        sess.user_email,
        salted_and_hashed_password,
        "ARTIST",
        acct_status,
        salt,
    )
    log_on(sess)
