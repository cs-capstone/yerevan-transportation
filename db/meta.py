from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# TODO: make singleton, static method
class DbSession:
    conn_str = 'postgresql://davidshadunts:123456@localhost:5432/transportation'

    def __init__(self):
        engine = create_engine(self.conn_str)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_session(self):
        return self.session
