from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

base=declarative_base()
class Product(base):
    __tablename__="Product"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String)
    price=Column(Integer)
    quantity=Column(Integer)
    category=Column(Integer)
    description=Column(String)
    
    
class User(base):
    __tablename__="User Authentication"
    email=Column(str, primary_key=True,index= True)
    password=Column(str)
    
    