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

#This function verifies if a user account is locked
def is_locked(email):
    connection = sqlite3.connect('trackmanagement.db')
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (email,))
    # Check if the acct_status of the user is locked
    if cursor.fetchone()[6] == "locked":
        return True
    else:
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

#This function is used by Administrators to unlock a user account  
def unlock_user_ID(user_id):
    connection = sqlite3.connect('trackmanagement.db')
    cursor = connection.cursor()
    query = """UPDATE users SET acct_status ='active' WHERE user_id = ?"""
    cursor.execute(query, (user_id,))
    # Commit the changes
    connection.commit()
    # Close the connection
    cursor.close()
    connection.close()
    return

def user_type(email): 
    connection = sqlite3.connect('trackmanagement.db')
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE email = ?"""
    cursor.execute(query, (email,))
    # Check if the user logged is an ADMIN or an ARTIST
    if cursor.fetchone()[5] == "ADMIN":
        return "ADMIN"
    else:
        return "ARTIST"
    return

#Display all locked user accounts to the system Admin
def view_all_locked_users():
    connection = sqlite3.connect('trackmanagement.db')
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE acct_status = 'locked'"""
    cursor.execute(query)
    # Get the results.
    results = cursor.fetchall()
    print(results)
    return

# Return the user details in a list[]
def get_user(user_id):
    connection = sqlite3.connect('trackmanagement.db')
    cursor = connection.cursor()
    query = """SELECT * FROM users WHERE user_id = ? """
    cursor.execute(query, (user_id,))
    # Get the results.
    results = cursor.fetchall()
    return results

def verify_password(salted_and_hashed_password):
    # TODO: verify encrypted string against db

    return True
