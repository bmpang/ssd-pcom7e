from api import initiate_session
from session import Session
from data_access.app_dao import admin_default

if __name__ == "__main__":
    #session = Session()
    #creates the table "users" and an admin system account named "admin@trackmanagement.com"
    admin_default()
    initiate_session()
