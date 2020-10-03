from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import database_info
from contextlib import contextmanager

username = database_info.get("username")
password = database_info.get("password")
host = database_info.get("host")
database = database_info.get("database")
engine = create_engine(f"mysql://{username}:{password}@{host}/{database}")
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

## Debug Mode Flag
debug = True

def test_connection():
    print(engine)

def create_tables():
    print("Creating Tables")
    Base.metadata.create_all(engine)
    print("Done")

@contextmanager
def get_session():
    print(f"Debug Mode: {debug}")
    session = Session()
    try:
        yield session
        if debug:
            session.rollback()
        else:
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class User(Base):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True, nullable=False)
    discord_id = Column('discord_id', String(100), nullable=False)
    forum_name = Column('forum_name', String(100), nullable=False)

    def set_forum_name(self, new_name):
        self.forum_name = new_name

    def get_forum_name(self):
        return self.forum_name

if __name__ == "__main__":
    create_tables()