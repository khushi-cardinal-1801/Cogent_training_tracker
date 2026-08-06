from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url="postgresql://postgres:ninja123@localhost:5433/products"

engine=create_engine(db_url)
session_local=sessionmaker(autocommit=False, autoflush=False, bind=engine)