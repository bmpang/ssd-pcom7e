from api import initiate_session
from data_access.app_dao import admin_default
from session import Session

if __name__ == "__main__":
    # session = Session()
    # creates the table "users" and an admin system account named "admin@trackmanagement.com"
    admin_default()
    initiate_session()
