from pydantic import BaseModel

class Product(BaseModel):
    id:int
    name:str
    price:int
    quantity:int
    category:str
    description:str
    
    # def __init__(self,id, name, price, quantity, category, description):
    #     self.id=id
    #     self.name=name
    #     self.price=price
    #     self.quantity=quantity
    #     self.category=category
    #     self.description=description