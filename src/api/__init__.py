from getpass import getpass

from data_access.app_dao import *
from model.artifact import Artifact
from model.copyrightable_material import (
    CopyrightableMaterial,
    FileSizeTooLargeException,
    InvalidCopyrightableMaterialTypeException,
)
from model.user import User
from util.encryption_util import create_salt, hash_data
from util.otp_util import send_otp_to_email


def initiate_session(sess):
    sess.user_email = input("Email:")
    if is_email_registered(sess.user_email):
        log_on(sess)
    else:
        register(sess)
    return


def log_on(sess):
    if is_locked(sess.user_email):
        print(
            "Your user account is currently locked - please reach out the system administrator to unlock your account"
        )
    else:
        salt = get_salt(sess.user_email)
        attempt = 1
        while attempt < 4:
            salted_and_hashed_password = hash_data(getpass("Enter password: "), salt)

            if user_auth(sess.user_email, salted_and_hashed_password):
                print("User logged in successfully")
                logged_user_as(sess.user_email)
                break
            else:
                print("Password incorrect - please try again!")
                attempt = attempt + 1
                if attempt == 4:
                    lock_user(sess.user_email)
                    print(
                        "Your user account has been locked - please reach out the system administrator to unlock your account"
                    )


def view_all_artifacts():
    artifact_summaries = []

    for summary_list in get_artifact_summaries():
        artifact_summaries.append(
            summary_list[2] + " for " + summary_list[1] + " by " + summary_list[0]
        )

    return artifact_summaries


def create_artifact(artist_id):
    title = input(
        "What is the title of the work you are uploading copyrightable material for?"
    )
    copyrightable_material_type = input(
        "What type of copyrightable material would you like to add - AUDIO, LYRICS, or SCORE?"
    )

    if artifact_exists(artist_id, title, copyrightable_material_type):
        print(
            "You already have an artifact for that copyrightable material. Please use the modify action to upload a new file."
        )

    file_path = input("Please input the filepath for your copyrightable material")

    try:
        copyrightable_material = CopyrightableMaterial(
            artist_id, title, file_path, copyrightable_material_type.upper()
        )
    except FileSizeTooLargeException:
        print("The file you have pathed too is too large.")
    except InvalidCopyrightableMaterialTypeException:
        print("Please pick a material type of AUDIO, LYRICS, or SCORE")

    artifact = Artifact(copyrightable_material)

    create_artifact(artifact)


def view_artists_artifacts(artist_id):
    artifact_summaries = []

    for summary_list in get_artists_artifact_summaries(artist_id):
        artifact_summaries.append(summary_list[1] + " for " + summary_list[0])

    return artifact_summaries


def download_artifact():
    # Todo
    return


def modify_artifact():
    input("Which")
    return


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
    salted_and_hashed_password = hash_data(getpass("Enter password: "), salt)
    first_name = input("Enter first name: ")
    surname = input("Enter last name: ")
    acct_status = "active"
    role = ""
    while role != "ARTIST" and role != "ADMIN":
        role = input("Enter ARTIST or ADMIN:")
        if role != "ARTIST" and role != "ADMIN":
            print("You must choose ARTIST or ADMIN")

    sess.role = role

    if role == "ARTIST":
        print("Welcome new Artist")
        addUser(
            first_name,
            surname,
            sess.user_email,
            salted_and_hashed_password,
            role,
            acct_status,
            salt,
        )
        sess.user_id = get_user_id(sess.user_email)

    if role == "ADMIN":
        print("Your Admin request will be sent to the Administor for approval")
