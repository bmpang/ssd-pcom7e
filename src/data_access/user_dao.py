import sys, sqlite3
from model.artist import Artist
sys.path.insert(0,"..")
connection = sqlite3.connect('trackmanagement.db')
cursor = connection.cursor()

# Check if the email is already registered.
def is_email_registered(email):
  
    # Create the table if it does not exist.
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            surname TEXT,
            email TEXT UNIQUE,
            password TEXT
        )"""
    )

    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (email,))

    # Get the results.
    results = cursor.fetchall()

    # Return True if the email is already registered, False otherwise.
    return len(results) > 0

#Enter a new user into the databse 
def addUser(first_name, surname, email, password):
    # Create the table if it does not exist.
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            surname TEXT,
            email TEXT UNIQUE,
            password TEXT
        )"""
    )
    query = """INSERT INTO users (first_name, surname, email, password) VALUES (?, ?, ?, ?)"""
    cursor.execute(query, (first_name, surname, email, password))
    # Commit the changes
    connection.commit()
    # Close the connection
    cursor.close()
    connection.close()
    print("User added successfully.")

def get_salt(user_email):
    # TODO: retrieve user salt string from db

    return "fake_salt"


def is_locked(user_email):
    # TODO: return lock status from db

    return False


def lock_user(user_email):
    # TODO: set user to locked in db

    return


def verify_password(salted_and_hashed_password):
    # TODO: verify encrypted string against db

    return True
