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
    if is_email_registered("admin@trackmanagement.com"):
        cursor.close()
        connection.close()
        return
    else:
        query = """INSERT INTO users (first_name, surname, email, password, role, acct_status, salt) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(
            query,
            (
                "Admin",
                "Admin",
                "admin@trackmanagement.com",
                "TMadmin20@",
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


# Check if the email is already registered.


def is_email_registered(email):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (email,))
    # Get the results.
    results = cursor.fetchall()
    # Return True if the email is already registered, False otherwise.
    return len(results) > 0


# Enter a new user into the databse


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


# create a function to check if the password provided an user match the password in the database?


def user_auth(email, user_password):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (email,))
    # Check if the password matches the one provided by the user
    if cursor.fetchone()[4] == user_password:
        return True
    else:
        return False


# This function gets the salt used for obfuscating a user's password to check the hash output of an inputted password
def get_salt(user_email):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (user_email,))

    return cursor.fetchone()[7]


# This function verifies if a user account is locked


def is_locked(email):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (email,))
    # Check if the acct_status of the user is locked
    if cursor.fetchone()[6] == "locked":
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

    return


def user_type(email):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (email,))
    # Check if the user logged is an ADMIN or an ARTIST
    if cursor.fetchone()[5] == "ADMIN":
        return "ADMIN"
    else:
        return "ARTIST"
    return


# Display all locked user accounts to the system Admin


def view_all_locked_users():
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE acct_status = 'locked'"""
    cursor.execute(query)
    # Get the results.
    results = cursor.fetchall()
    print(results)
    return


# Return the user details in a list[]


def get_user(user_id):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE user_id = ? """
    cursor.execute(query, (user_id,))
    # Get the results.
    results = cursor.fetchall()
    return results


# Fetch a user's id given their email


def get_user_id(email):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ? """
    cursor.execute(query, (email,))

    return cursor.fetchone()[7]


# Boot strap the table that holds artifacts for copyrightable material


def create_artifacts_table():
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()

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

    cursor.close()
    connection.close()


def get_artifact_id(artist_id, title, type):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT artifact_id from artifacts where artist_id = ? and title = ? and type = ?"""

    cursor.execute(query, (artist_id, title, type))

    result = cursor.fetchone()

    # Close the connection
    cursor.close()
    connection.close()

    if result:
        return result[0]
    else:
        return None


def get_checksum(artist_id, title, type):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """SELECT checksum from artifacts where artist_id = ? and title = ? and type = ?"""

    cursor.execute(query, (artist_id, title, type))

    result = cursor.fetchone()

    # Close the connection
    cursor.close()
    connection.close()

    if result:
        return result[0]
    else:
        return None


def artifact_exists(artist_id, title, type):
    return get_artifact_id(artist_id, title, type) is not None


def create_artifact(artifact):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """INSERT INTO artifacts (artist_id, title, type, file_size_bytes, file_extension, checksum, encrypted_data) VALUES (?, ?, ?, ?)"""
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
    if len(results) == 0:
        return
    cursor.close()
    connection.close()
    return results

# Get summaries for all of one artist's copyrightable material artifacts


def get_artists_artifact_summaries(artist_id):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """title, type FROM artifacts where artist_id = ?"""
    cursor.execute(query, (artist_id,))

    results = cursor.fetchall()

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

    cursor.close()
    connection.close()
    return file_info


def update_artifact(artifact):
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()
    query = """UPDATE artifact SET file_size_bytes = ?, file_extension = ?, checksum = ?, encrypted_data = ? WHERE artist_id = ? and title = ? and type = ?"""

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


# Create the artifact audit table


def create_artifacts_audit_table():
    connection = sqlite3.connect("trackmanagement.db")
    cursor = connection.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS artifact_audit (
            audit INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id INTEGER,
            artifact_id INTEGER
            action TEXT,
            time TEXT,
            
            FOREIGN KEY (artist_id)
                REFERENCES users (user_id)

            FOREIGN KEY (artifact_id)
                REFERENCES artifacts (artifact_id)
        )"""
    )

    cursor.close()
    connection.close()


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
