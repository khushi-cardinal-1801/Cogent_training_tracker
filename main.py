from fastapi import Depends,FastAPI
from model import Product
from database import session_local, engine
import database_model
from sqlalchemy.orm import Session
obj=FastAPI()

database_model.base.metadata.create_all(bind=engine)

@obj.get("/")

def welcome():
    return ("Hey we are staring with Fast API")

products=[
    Product(id=3,name="bread",price=20,quantity=10,category=1,description="breakfast eating fmcg product"),
    Product(id=4,name="milk", price=36, quantity="1", category=2, description="day to day eating products"),
]


def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()
        
def init_db():
    db=session_local()
    count=db.query(database_model.Product).count 
    if count==0:
        for i in products:
            db.add(database_model.Product(**i.model_dump()))  
    db.commit()
        
init_db()

@obj.get("/products")

def prod_name(db: Session=Depends(get_db)):
    db_products=db.query(database_model.Product).all()
    return db_products

@obj.get("/product/{id}")

def get_product(id:int, db:Session=Depends(get_db)):
    selected_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if(selected_product):
        return selected_product
    return "product not found"
    

@obj.post("/product")
def app_prod(productss:Product, db:Session=Depends(get_db)):
    db.add(database_model.Product(**productss.model_dump()))
    db.commit()
    return productss
    
    
@obj.put("/product")
def update_prod(id:int,productss:Product, db:Session=Depends(get_db)):
    selected_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if selected_product:
        selected_product.name=productss.name
        selected_product.category=productss.category
        selected_product.price=productss.price
        selected_product.quantity=productss.quantity
        selected_product.description=productss.description
        
        return "product updated successfully"
    
    else:
        return "product id didnt match"
        
        

@obj.delete("/Product")
def delete_prod(id:int):
    for i in range(len(products)):
        if(products[i].id==id):
            del products[i]
            return "Products deleted successfully"
        
    return "Product id not found"
        
    