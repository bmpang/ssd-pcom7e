#ROLE = ["ARTIST", "ADMIN"]

#Class User used for new users including Artist & Administrators
class User:
    def __init__(self, user_id, first_name, surname, email, password):
        self.user_id = user_id
        self.first_name = first_name
        self.surname = surname
        self.email = email
        self.password = password
        #self.role = ROLE