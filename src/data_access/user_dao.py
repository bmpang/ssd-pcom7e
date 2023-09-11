import sys, sqlite3
from model.artist import Artist
sys.path.insert(0,"..")
connection = sqlite3.connect('trackmanagement.db')
cursor = connection.cursor()
obj = Artist(3)
print(obj.getVal())

#how to represent a one to N relationship between two classes?

#Enter a new user into the databse 
#def addUser(self):
    cursor.execute("""
    INSERT INTO users VALUES ({}, {},{},{})""".format())
    connection.commit()

#def get_salt(user_email):
    # TODO: retrieve user salt string from db

    return "fake_salt"


#def is_locked(user_email):
    # TODO: return lock status from db

    return False


#def lock_user(user_email):
    # TODO: set user to locked in db

    return


#def verify_password(salted_and_hashed_password):
    # TODO: verify encrypted string against db

    return True

#connection.close()