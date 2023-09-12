from api import initiate_session, login_session
from session import Session

if __name__ == "__main__":
    session = Session()
    login_session(session)
    #initiate_session(session)
