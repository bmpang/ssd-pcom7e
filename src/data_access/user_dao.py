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