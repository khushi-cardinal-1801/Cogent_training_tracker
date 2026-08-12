from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from database import base
class Product(base):
    __tablename__="Product"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String)
    price=Column(Integer)
    quantity=Column(Integer)
    category=Column(Integer)
    description=Column(String)
   
class UserDB(base):
    __tablename__="User"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    
    

    
    