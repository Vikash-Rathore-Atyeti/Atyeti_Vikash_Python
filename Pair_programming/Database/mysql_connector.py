from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus 
 
class DBConnection:
    def __init__(self, user, password, host, database):
        password = quote_plus(password)
        url = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
        self.engine = create_engine(url)
        self.Session = sessionmaker(bind=self.engine)
 
    def get_session(self):
        return self.Session()

