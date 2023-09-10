from data_access.user_dao import get_salt, is_locked, lock_user, verify_password
from getpass import getpass
from util.encryption_util import hash_data
from util.otp_util import send_otp_to_email


def initiate_session(session, failures=0):
    if failures == 3:
        print(
            "You have failed to log in 3 times in a row, your account has been locked"
        )
        lock_user(session.user_email)
        raise Exception

    if not session.user_email:
        session.user_email = input("Email: ")

    if is_locked(session.user_email):
        print(
            "Your account is locked, please reach out to an administrator for help regaining access"
        )
        raise Exception

    if not session.password_verified:
        user_salt = get_salt(session.user_email)
        # The password is salted immediately so that the user's plain password is never stored in memory
        # the python native getpass method also hides the text from the cli
        salted_and_hashed_password = hash_data(getpass(prompt="Password: "), user_salt)

        if not verify_password(salted_and_hashed_password):
            initiate_session(session, failures + 1)
        else:
            session.password_verified = True

    if not session.otp_verified:
        print("Sending you a one time passcode")
        otp_code = send_otp_to_email(session.user_email)

        input_otp = input("OTP Code: ")

        if input_otp != otp_code:
            initiate_session(session, failures + 1)
        else:
            session.otp_verified = True


def create_artist():
    # Todo: Brandon
    return


def modify_artist():
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


def unlock_user():
    # Todo: Lucas
    return


def register():
    # Todo: Lucas
    return
