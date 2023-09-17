from api import *
from data_access.app_dao import admin_default, create_artifacts_table
from session import Session


# sets up the database initially
def bootstrap_database():
    # creates the table "users" and an admin system account named "admin@trackmanagement.com"
    admin_default()
    # creates the table for copyrightable material artifacts
    create_artifacts_table()


def prompt():
    if sess.role == "ARTIST":
        should_call_create_artifact = (
            input("Would you like to add a new track - Y/N?").upper() == "Y"
        )

        if should_call_create_artifact:
            create_artifact(sess.user_id)

    else:
        print(
            "Here are the summaries of all the copyrightable material artifacts managed in the system:"
        )
        view_all_artifacts()
        print("All locked users:")
        view_all_locked_users()
        unlock_user_id = input(
            "Enter the ID of the user you wish to unlock or '0' to cancel:"
        )
        unlock_user(unlock_user_id)


if __name__ == "__main__":
    bootstrap_database()

    sess = Session()
    initiate_session(sess)

    if sess.user_id:
        prompt()
