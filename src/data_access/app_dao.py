import sqlite3
import sys

sys.path.insert(0, "..")
connection = sqlite3.connect("trackmanagement.db")
cursor = connection.cursor()

# creates an application "admin" user when the app is run


def admin_default():
    # Create the table if it does not exist.
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            surname TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT,
            acct_status TEXT,
            salt TEXT
        )"""
    )

    # If the default admin user has already been created, exit early
    if is_email_registered("admin@trackmanagement.com"):
        cursor.close()
        connection.close()
        return
    else:
        # Create a new record for the admin user
        query = """INSERT INTO users (first_name, surname, email, password, role, acct_status, salt) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(
            query,
            (
                "Admin",
                "Admin",
                "admin@trackmanagement.com",
                "e0a89c103f84f78e296a6a7257fdb28b43f7b0f6f89145756d40bb6bd867700c",
                "ADMIN",
                "active",
                "QiZ2wX4v",
            ),
        )

        # Commit the changes
        connection.commit()

        # Close the connection
        cursor.close()
        connection.close()
        print("Defaut Admin added to the database")


# Check if an email is already registered.
def is_email_registered(email):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (email,))

    # Get the results.
    results = cursor.fetchall()

    # Close the connection
    cursor.close()
    connection.close()

    # Return True if there are any records matching the email, False otherwise.
    return len(results) > 0


# Enter a new user into the databse based off inputted details
def addUser(first_name, surname, email, password, role, acct_status, salt):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """INSERT INTO users (first_name, surname, email, password, role, acct_status, salt) VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(
        query, (first_name, surname, email, password, role, acct_status, salt)
    )

    # Commit the changes
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()
    print("User added successfully.")


# create a function to check if the password provided an user match the password in the database
# note that both the supplied password and the one in the db would have been salted and hashed at this point
# and it would not be possible to decrypt the strings to plain text
def user_auth(email, user_password):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (email,))
    stored_password = cursor.fetchone()[4]

    # Close the connection
    cursor.close()
    connection.close()

    # Check if the password matches the one provided by the user
    if stored_password == user_password:
        return True
    else:
        return False


# This function gets the salt used for obfuscating a user's password to check the hash output of an inputted password
def get_salt(user_email):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (user_email,))

    salt = cursor.fetchone()[7]

    # Close the connection
    cursor.close()
    connection.close()

    return salt


# Get role
def get_role(user_email):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT role FROM users WHERE email = ?"""
    cursor.execute(query, (user_email,))

    role = cursor.fetchone()[0]

    # Close the connection
    cursor.close()
    connection.close()

    return role


def get_user_name(user_email):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT first_name FROM users WHERE email = ?"""
    cursor.execute(query, (user_email,))

    user_name = cursor.fetchone()[0]

    # Close the connection
    cursor.close()
    connection.close()

    return user_name


# This function verifies if a user account is locked
def is_locked(email):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (email,))
    status = cursor.fetchone()[6]

    # Close the connection
    cursor.close()
    connection.close()

    # Check if the acct_status of the user is locked
    if status == "locked":
        return True
    else:
        return False


# This function locks a user account after 3 unsuccessful login attempts
def lock_user(email):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """UPDATE users SET acct_status ='locked' WHERE email = ?"""
    cursor.execute(query, (email,))

    # Commit the changes
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

    return


# This function is used by Administrators to unlock a user account
def unlock_user_ID(user_id):
    if view_all_locked_users() == None:
        print("There are no locked users to unlock!")
    else:
        connection = sqlite3.connect("trackmanagement.db")
        cursor = connection.cursor()
        query = """UPDATE users SET acct_status ='active' WHERE user_id = ?"""
        cursor.execute(query, (user_id,))

        # Commit the changes
        connection.commit()

        # Close the connection
        cursor.close()
        connection.close()

        print(f"The user {get_user(user_id)[0]} has been unlocked")


# Display all locked user accounts to the system Admin
def view_all_locked_users():
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE acct_status = 'locked'"""
    cursor.execute(query)

    # Get the results.
    results = cursor.fetchall()
    print(results)

    # Close the connection
    cursor.close()
    connection.close()


# Return the user details in a list[]
def get_user(user_id):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE user_id = ? """
    cursor.execute(query, (user_id,))

    # Get the results.
    results = cursor.fetchall()

    # Close the connection
    cursor.close()
    connection.close()

    return results


# Fetch a user's id given their email
def get_user_id(email):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ? """
    cursor.execute(query, (email,))

    id = cursor.fetchone()[0]

    # Close the connection
    cursor.close()
    connection.close()

    return id


# Boot strap the table that holds artifacts for copyrightable material
def create_artifacts_table():
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()

    # Create the table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS artifacts (
            artifact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id INTEGER,
            title TEXT,
            type TEXT,
            file_size_bytes INTEGER,
            file_extension TEXT,
            checksum TEXT UNIQUE,
            encrypted_data TEXT,
            
            FOREIGN KEY (artist_id)
                REFERENCES users (user_id)
        )"""
    )

    # Close connections
    cursor.close()
    connection.close()


# Get an id for an artifact given an artist, title, and material type
def get_artifact_id(artist_id, title, type):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT artifact_id from artifacts where artist_id = ? and title = ? and type = ?"""

    cursor.execute(query, (artist_id, title, type))

    result = cursor.fetchone()

    # Close the connection
    cursor.close()
    connection.close()

    # If there were no hits, there is no material matching the given specifications
    if result:
        return result[0]
    else:
        return None


# Retrieve the checksum for the file ingested for an artifact
def get_checksum(artist_id, title, type):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT checksum from artifacts where artist_id = ? and title = ? and type = ?"""

    cursor.execute(query, (artist_id, title, type))

    result = cursor.fetchone()

    # Close the connection
    cursor.close()
    connection.close()

    # If there is no matching record given the specifications, there is no checksum to return
    if result:
        return result[0]
    else:
        return None


# Check whether an artifact exists or not
def artifact_exists(artist_id, title, type):
    # If there is no id returned, no record exists
    return get_artifact_id(artist_id, title, type) is not None


# Create a record for a new artifact
def create_artifact_row(artifact):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """INSERT INTO artifacts (artist_id, title, type, file_size_bytes, file_extension, checksum, encrypted_data) VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(
        query,
        (
            artifact.artist_id,
            artifact.title,
            artifact.copyrightable_material_type,
            artifact.file_size_bytes,
            artifact.file_extension,
            artifact.checksum,
            artifact.encrypted_data,
        ),
    )

    # Commit the changes
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()


# Get summaries for all copyrightable material artifacts
def get_artifact_summaries():
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT users.first_name || ' ' || users.surname as artist_name, artifacts.title as title, artifacts.type as type FROM artifacts inner join users on artifacts.artist_id = users.user_id"""
    cursor.execute(
        query,
    )

    results = cursor.fetchall()

    # Close the connection
    cursor.close()
    connection.close()

    # If there are no results, return None instead of an empty list
    if len(results) == 0:
        return None

    return results


# Get summaries for all of one artist's copyrightable material artifacts
def get_artists_artifact_summaries(artist_id):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT title, type FROM artifacts where artist_id = ?"""
    cursor.execute(query, (artist_id,))

    results = cursor.fetchall()

    # Close the connection
    cursor.close()
    connection.close()

    return results


# get the file info for an artifact
def get_file_info_from_artifact(artist_id, title, type):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT title, type, file_extension, encrypted_data from artifacts where artist_id = ? and title = ? and type = ?"""
    cursor.execute(query, (artist_id, title, type))

    file_info = cursor.fetchone()

    # Close the connection
    cursor.close()
    connection.close()

    return file_info


def update_artifact(artifact):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """UPDATE artifacts SET file_size_bytes = ?, file_extension = ?, checksum = ?, encrypted_data = ? WHERE artist_id = ? and title = ? and type = ?"""

    cursor.execute(
        query,
        (
            artifact.file_size_bytes,
            artifact.file_extension,
            artifact.checksum,
            artifact.encrypted_data,
            artifact.artist_id,
            artifact.title,
            artifact.copyrightable_material_type,
        ),
    )

    # Commit the changes
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()


# Delete an artifact
def delete_artifact_row(artist_id, title, copyrightable_material_type):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """DELETE FROM artifacts WHERE artist_id = ? and title = ? and type = ?"""
    cursor.execute(query, (artist_id, title, copyrightable_material_type))

    # Commit the changes
    connection.commit()
    # Close the connection
    cursor.close()
    connection.close()


# Create the artifact audit table
def create_artifacts_audit_table():
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS artifact_audit (
            audit INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id INTEGER,
            artifact_id INTEGER,
            action TEXT,
            time TEXT,
            
            FOREIGN KEY (artist_id)
                REFERENCES users (user_id)

            FOREIGN KEY (artifact_id)
                REFERENCES artifacts (artifact_id)
        )"""
    )

    # Close the connection
    cursor.close()
    connection.close()


# Create a new time stamp record for an action taken against an artifact
def create_artifact_audit_log(artist_id, artifact_id, action, time):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()

    query = """INSERT INTO artifact_audit (artist_id, artifact_id, action, time) VALUES (?, ?, ?, ?)"""
    cursor.execute(
        query,
        (artist_id, artifact_id, action, time),
    )

    # Commit the changes
    connection.commit()
    # Close the connection
    cursor.close()
    connection.close()
