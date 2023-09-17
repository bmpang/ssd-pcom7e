from getpass import getpass

from data_access.app_dao import *
from model.user import User
from util.encryption_util import hash_data
from util.otp_util import send_otp_to_email


def initiate_session(failures=0):
    email = input("Email:")
    if is_email_registered(email):
        if is_locked(email):
            print(
                "Your user account is currently locked - please reach out the system administrator to unlock your account"
            )
        else:
            attempt = 1
            while attempt < 4:
                user_password = input("Enter your user password:")
                if user_auth(email, user_password):
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

    # if failures == 3:
    #     print(
    #         "You have failed to log in 3 times in a row, your account has been locked"
    #     )
    #     lock_user(session.user_email)
    #     raise Exception

    # if not session.user_email:
    #     session.user_email = input("Email: ")

    # if is_locked(session.user_email):
    #     print(
    #         "Your account is locked, please reach out to an administrator for help regaining access"
    #     )
    #     raise Exception

    # if not session.password_verified:
    #     user_salt = get_salt(session.user_email)
    #     # The password is salted immediately so that the user's plain password is never stored in memory
    #     # the python native getpass method also hides the text from the cli
    #     salted_and_hashed_password = hash_data(getpass(prompt="Password: "), user_salt)

    #     if not verify_password(salted_and_hashed_password):
    #         initiate_session(session, failures + 1)
    #     else:
    #         session.password_verified = True

    # if not session.otp_verified:
    #     print("Sending you a one time passcode")
    #     otp_code = send_otp_to_email(session.user_email)

    #     input_otp = input("OTP Code: ")

    #     if input_otp != otp_code:
    #         initiate_session(session, failures + 1)
    #     else:
    #         session.otp_verified = True


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


def create_artist():
    # Todo: Brandon - this is already done
    return


# we dont need to modify an artist


def modify_artist():
    # Todo: Brandon - this is not needed
    return


def view_all_tracks():
    # Todo: Brandon
    return


def create_artifact():
    # Todo: Brandon
    return


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
    password = input("Enter password: ")
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
        addUser(first_name, surname, email, password, role, acct_status)
    if role == "ADMIN":
        print("Your Admin request will be sent to the Administor for approval")
    return
