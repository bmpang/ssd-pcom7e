from api import *
import os
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

def artist_menu():
    os.system('cls')
    print(f"Wecolme {sess.user_name} to the Track Management System:\n\n")
    print("|--------------------------------------------------------------------------------|")
    print("[1] - Add a new copyrightable material artifact")
    print("[2] - Display your currently managed copyrightable material")
    print("[3] - Download copyrightable material from a currently managed artifact")
    print("[4] - Upload a new version of a currently managed copyrightable material")
    print("[5] - Delete a currently managed copyrightable material")
    print("[0] - Logout and exit the program")
    print("|--------------------------------------------------------------------------------|")
    choice = input("Enter your choise: ")
    return choice
 
def admin_menu():
    os.system('cls')
    print(f"Wecolme {sess.user_name} to the Track Management System:\n\n")
    print("|--------------------------------------------------------------------------------|")
    print("[1] - Display all artifacts managed in the system")
    print("[2] - View all locked user accounts")
    print("[3] - Unlock a user")
    print("[0] - Logout and exit the program")
    print("|--------------------------------------------------------------------------------|")
    choice = input("Enter your choise: ")
    return choice

# This function is used as a main menu that prompts users for what actions they wish to take
def prompt():
    # Artists and admins are given different options
    if sess.role == "ARTIST":
        choice = artist_menu()
        # Check if a user wants to create a new artifact or not
        if choice == "1":
            create_artifact(sess.user_id)
            input("Press any key to continue...")
         # Check if a user wants to view their existing artifacts or not
        elif choice == "2":
            view_artists_artifacts(sess.user_id)
            input("Press any key to continue...")
        # Check if a user would like to download an existing artifact
        elif choice == "3":
            download_from_artifact(sess.user_id)
            input("Press any key to continue...")
        # Check if a user would like to modify an existing artifact
        elif choice == "4":
            modify_artifact(sess.user_id)
            input("Press any key to continue...")
        # Check if a user would like to delete one of their artifacts
        elif choice == "5":
            delete_artifact(sess.user_id)
        elif choice == "0":
            sess.user_id = None
            return      
    elif sess.role == 'ADMIN':
        choice = admin_menu()
        # Check if an admin would like to list all artifacts in the system
        if choice == "1":
            view_all_artifacts()
            input("Press any key to continue...")
        # Check if an admin would like to list all users currently locked out of their accounts
        elif choice == "2":
            view_all_locked_users()
            input("Press any key to continue...")
        # Check if an admin would like to unlock a specific user
        elif choice == "3":
            unlock_user_id = input("Choose the userID you wish to unlock: ")
            unlock_user(unlock_user_id)
            input("Press any key to continue...")
        # Check if a user would like to modify an existing artifact
        elif choice == "0":
            sess.user_id = None
            return      


# This is the method actually called when the app is ran.
if __name__ == "__main__":
    # Create required tables and default admin account if they do not exist
    bootstrap_database()

    # Determine the user's identity via log on or registration in order to figure out what actions to prompt
    sess = Session()
    initiate_session(sess)

    # Once the user's identity is known, loop the main menu for them to take actions
    while sess.user_id:
        prompt()
