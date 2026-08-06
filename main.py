from fastapi import FastAPI
from model import Product

obj=FastAPI()
@obj.get("/")


def welcome():
    return ("Hey we are staring with Fast API")

products=[
    Product(id=1,name="bread",price=20,quantity=10,category="fmcg",description="breakfast eating fmcg product"),
    Product(id=2,name="milk", price=36, quantity="1", category="FMCG", description="day to day eating products"),
]
@obj.get("/products")

def prod_name():
    return products

@obj.get("/product/{id}")

def get_product(id:int):
    for i in products:
        if(id==products[id]):
            return products[id]
    return "product not found"
    

@obj.post("/product")
def app_prod(productss:Product):
    products.append(productss)
    return productss
    
    
@obj.put("/product")
def update_prod(id:int,productss:Product):
    for i in range(len(products)):
        if(products[i].id==id):
            products[i]=productss
            return "product updated successfully"
        
    return "product id didnt match"

@obj.delete("/Product")
def delete_prod(id:int):
    for i in range(len(products)):
        if(products[i].id==id):
            del products[i]
            return "Products deleted successfully"
        
    return "Product id not found"
        
    