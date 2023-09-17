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


def initiate_session(failures=0):
    email = input("Email:")
    if is_email_registered(email):
        if is_locked(email):
            print(
                "Your user account is currently locked - please reach out the system administrator to unlock your account"
            )
        else:
            salt = get_salt(email)
            attempt = 1
            while attempt < 4:
                salted_and_hashed_password = hash_data(
                    getpass("Enter password: "), salt
                )

                if user_auth(email, salted_and_hashed_password):
                    print("User logged in successfully")
                    logged_user_as(email)
                    break
                else:
                    print("Password incorrect - please try again!")
                    attempt = attempt + 1
                    if attempt == 4:
                        lock_user(email)
                        print(
                            "Your user account has been locked - please reach out the system administrator to unlock your account"
                        )
    else:
        register(email)
    return


def logged_user_as(email):
    if user_type(email) == "ADMIN":
        view_all_tracks()
        print("All locked users:")
        view_all_locked_users()
        unlock_user_id = input(
            "Enter the ID of the user you wish to unlock or '0' to cancel:"
        )
        unlock_user(unlock_user_id)
        print(f"The user {get_user(unlock_user_id)[0]} has been unlocked")
    return


def view_all_tracks():
    # Todo: Brandon
    return


def create_artifact():
    copyrightable_material_type = input(
        "What type of copyrightable material would you like to add - AUDIO, LYRICS, or SCORE?"
    )
    file_path = input("Please input the filepath for your copyrightable material")

    try:
        copyrightable_material = CopyrightableMaterial(
            file_path, copyrightable_material_type.upper()
        )
    except FileSizeTooLargeException:
        print("The file you have pathed too is too large.")
    except InvalidCopyrightableMaterialTypeException:
        print("Please pick a material type of AUDIO, LYRICS, or SCORE")

    artifact = Artifact(copyrightable_material)

    create_artifact(artifact)


def get_artifact():
    # Todo
    return


def modify_artifact():
    # Todo: Brandon
    return


# This function unlocks a user account which was locked after 3 incorrect provided password


def unlock_user(user_id):
    unlock_user_ID(user_id)
    return


# This funtion registers a new user and adds them to the database table users


def register(email):
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
    if role == "ARTIST":
        print("Welcome new Artist")
        addUser(
            first_name,
            surname,
            email,
            salted_and_hashed_password,
            role,
            acct_status,
            salt,
        )
    if role == "ADMIN":
        print("Your Admin request will be sent to the Administor for approval")
    return
