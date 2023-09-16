import sys, sqlite3
from model.artist import Artist
sys.path.insert(0,"..")
connection = sqlite3.connect('trackmanagement.db')
cursor = connection.cursor()

#creates an application "admin" user when the app is run
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
            acct_status TEXT
        )"""
    )
    if is_email_registered("admin@trackmanagement.com"):
        cursor.close()
        connection.close()
        return 
    else:
        query = """INSERT INTO users (first_name, surname, email, password, role, acct_status) VALUES (?, ?, ?, ?, ?, ?)"""
        cursor.execute(query, ("Admin", "Admin", "admin@trackmanagement.com", "TMadmin20@", "ADMIN", "active"))
        # Commit the changes
        connection.commit()
        # Close the connection
        cursor.close()
        connection.close()
        print("Defaut Admin added to the database")

# Check if the email is already registered.
def is_email_registered(email):  
    connection = sqlite3.connect('trackmanagement.db')
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (email,))
    # Get the results.
    results = cursor.fetchall()
    # Return True if the email is already registered, False otherwise.
    return len(results) > 0

#Enter a new user into the databse 
def addUser(first_name, surname, email, password, role, acct_status):
    connection = sqlite3.connect('trackmanagement.db')
    cursor = connection.cursor()
    query = """INSERT INTO users (first_name, surname, email, password, role, acct_status) VALUES (?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (first_name, surname, email, password, role, acct_status))
    # Commit the changes
    connection.commit()
    # Close the connection
    cursor.close()
    connection.close()
    print("User added successfully.")

#create a function to check if the password provided an user match the password in the database?
def user_auth(email, user_password):
    connection = sqlite3.connect('trackmanagement.db')
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (email,))
    # Check if the password matches the one provided by the user
    if cursor.fetchone()[4] == user_password:
        return True
    else:
        return False
    

def get_salt(user_email):
    # TODO: retrieve user salt string from db

    return "fake_salt"


def is_locked(user_email):
    # TODO: return lock status from db

    return False

#This function locks a user account after 3 unsuccessful login attempts 
def lock_user(email):
    connection = sqlite3.connect('trackmanagement.db')
    cursor = connection.cursor()
    query = """UPDATE users SET acct_status ='locked' WHERE email = ?"""
    cursor.execute(query, (email,))
    # Commit the changes
    connection.commit()
    # Close the connection
    cursor.close()
    connection.close()
    return

def verify_password(salted_and_hashed_password):
    # TODO: verify encrypted string against db

    return True
