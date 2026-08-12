from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
db_url=os.getenv("db_url")

base=declarative_base()

engine=create_engine(db_url)
session_local=sessionmaker(autocommit=False, autoflush=False, bind=engine)