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


def prompt():
    if sess.role == "ARTIST":
        should_call_create_artifact = (
            input(
                "Would you like to add a new copyrightable material artifact - Y/N? "
            ).upper()
            == "Y"
        )

        if should_call_create_artifact:
            create_artifact(sess.user_id)

        should_call_view_artists_artifacts = (
            input(
                "Would you like to see your currently managed copyrightable material - Y/N? "
            ).upper()
            == "Y"
        )

        if should_call_view_artists_artifacts:
            view_artists_artifacts(sess.user_id)

        should_call_download_from_artifact = (
            input(
                "Would you like to download copyrightable material from a currently managed artifact - Y/N? "
            ).upper()
            == "Y"
        )

        if should_call_download_from_artifact:
            download_from_artifact(sess.user_id)

        should_call_modify_artifact = (
            input(
                "Would you like to upload a new version of a currently managed copyrightable material - Y/N? "
            ).upper()
            == "Y"
        )

        if should_call_modify_artifact:
            modify_artifact(sess.user_id)

        should_call_delete_artifact = (
            input(
                "Would you like to delete a currently managed copyrightable material - Y/N? "
            ).upper()
            == "Y"
        )

        if should_call_delete_artifact:
            delete_artifact(sess.user_id)
    else:
        print(
            "Here are the summaries of all the copyrightable material artifacts managed in the system:"
        )
        view_all_artifacts()
        print("All locked users:")
        view_all_locked_users()
        unlock_user_id = input(
            "Enter the ID of the user you wish to unlock or '0' to cancel: "
        )
        if unlock_user_id != "0":
            unlock_user(unlock_user_id)


if __name__ == "__main__":
    bootstrap_database()

    sess = Session()
    initiate_session(sess)

    if sess.user_id:
        prompt()
