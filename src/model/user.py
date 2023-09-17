# ROLE = ["ARTIST", "ADMIN"]

# Class User used for new users including Artist & Administrators
class User:
    def __init__(self, first_name, surname, email, password):
        self.first_name = first_name
        self.surname = surname
        self.email = email
        self.password = password
        # self.role = ROLE
