from api import *
from data_access.app_dao import (
    admin_default,
    create_artifacts_audit_table,
    create_artifacts_table,
)
from session import Session


# sets up the database initially
def bootstrap_database():
    # creates the table "users" and an admin system account named "admin@trackmanagement.com"
    admin_default()

    # creates the table for copyrightable material artifacts
    create_artifacts_table()

    # creates the artifact audit table for logging timestamps
    create_artifacts_audit_table()


# This function is used as a main menu that prompts users for what actions they wish to take
def prompt():
    # Artists and admins are given different options
    if sess.role == "ARTIST":
        # Check if a user wants to create a new artifact or not
        should_call_create_artifact = (
            input(
                "Would you like to add a new copyrightable material artifact - Y/N? "
            ).upper()
            == "Y"
        )
        if should_call_create_artifact:
            create_artifact(sess.user_id)
            return

        # Check if a user wants to view their existing artifacts or not
        should_call_view_artists_artifacts = (
            input(
                "Would you like to see your currently managed copyrightable material - Y/N? "
            ).upper()
            == "Y"
        )
        if should_call_view_artists_artifacts:
            view_artists_artifacts(sess.user_id)
            return

        # Check if a user would like to download an existing artifact
        should_call_download_from_artifact = (
            input(
                "Would you like to download copyrightable material from a currently managed artifact - Y/N? "
            ).upper()
            == "Y"
        )
        if should_call_download_from_artifact:
            download_from_artifact(sess.user_id)
            return

        # Check if a user would like to modify an existing artifact
        should_call_modify_artifact = (
            input(
                "Would you like to upload a new version of a currently managed copyrightable material - Y/N? "
            ).upper()
            == "Y"
        )
        if should_call_modify_artifact:
            modify_artifact(sess.user_id)
            return

        # Check if a user would like to delete one of their artifacts
        should_call_delete_artifact = (
            input(
                "Would you like to delete a currently managed copyrightable material - Y/N? "
            ).upper()
            == "Y"
        )
        if should_call_delete_artifact:
            delete_artifact(sess.user_id)
            return
    else:
        # Check if an admin would like to list all artifacts in the system
        should_call_view_all_artifacts = (
            input(
                "Would you like to view all artifacts managed in the system - Y/N? "
            ).upper()
            == "Y"
        )
        if should_call_view_all_artifacts:
            view_all_artifacts()
            return

        # Check if an admin would like to list all users currently locked out of their accounts
        should_call_view_all_locked_users = (
            input("Would you like to view all locked user accounts - Y/N? ").upper()
            == "Y"
        )
        if should_call_view_all_locked_users:
            view_all_locked_users()
            return

        # Check if an admin would like to unlock a specific user
        should_call_unlock_user_id = (
            input("Would you like to unlock a user - Y/N? ").upper() == "Y"
        )
        if should_call_unlock_user_id:
            unlock_user_id = input(
                "Enter the ID of the user you wish to unlock or '0' to cancel: "
            )

            unlock_user(unlock_user_id)
            return


# This is the method actually called when the app is ran.
if __name__ == "__main__":
    # Create required tables and default admin account if they do not exist
    bootstrap_database()

    # Determine the user's identity via log on or registration in order to figure out what actions to prompt
    sess = Session()
    initiate_session(sess)

    # Once the user's identity is known, loop the main menu for them to take actions
    while True:
        prompt()
