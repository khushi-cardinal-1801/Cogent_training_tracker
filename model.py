from pydantic import BaseModel, EmailStr, Field, field_validator


class Product(BaseModel):
    id:int
    name:str
    price:int=Field(gt=0)
    quantity:int=Field(gt=0)
    category:int
    description:str
    
    # def __init__(self,id, name, price, quantity, category, description):
    #     self.id=id
    #     self.name=name
    #     self.price=price
    #     self.quantity=quantity
    #     self.category=category
    #     self.description=description
    
    
class User(BaseModel):
    email:EmailStr
    password:str
    
    @field_validator("password")
    @classmethod
    def pass_val(cls,value):
        if(len(value)<8):
            raise ValueError("Password should be greater than 7 digits")
        return value
    
        
