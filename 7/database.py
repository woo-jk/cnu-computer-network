from curses import echo
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# user_id = os.environ.get("MYSQL_USER")
# user_pw = os.environ.get('MYSQL_PASSWORD')
# port = os.environ.get('MYSQL_PORT')
# db = os.environ.get('MYSQL_DATABASE') 

# SQLALCHEMY_DATABASE_URL = 'mariadb+mariadbconnector://pasteuser:user-secret-pw@127.0.0.1:3306/pastebin'
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://pasteuser:user-secret-pw@127.0.0.1:3306/pastebin"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

