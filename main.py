from fastapi import Depends,FastAPI
from model import Product
from database import session_local, engine
import database_model
from sqlalchemy.orm import Session
from auth import router
from auth import token_verfication
from redis_client import redis_client
import json
from arq import create_pool
from arq.connections import RedisSettings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lisfespan(app:FastAPI):
    app.state.arq_pool=await create_pool(
        RedisSettings(
            host="localhost",
            port=6379
        )
    )
    yield
    await app.state.arq_pool.close()
    
obj=FastAPI(lifespan=lisfespan)

database_model.base.metadata.create_all(bind=engine)
obj.include_router(router)

@obj.get('/redis-test')

async def redis_test():
    await redis_client.set("test-key", "radis is working")
    value=await redis_client.get("test-key")
    return value

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
    count=db.query(database_model.Product).count()
    if count==0:
        for i in products:
            db.add(database_model.Product(**i.model_dump()))  
    db.commit()
        
init_db()

@obj.get("/products")

async def prod_name(page:int=1,
              limit:int=5,
              email:str=Depends(token_verfication),
              db: Session=Depends(get_db)
              ):
    skip=(page-1)*limit
    cache_key = f"products:page:{page}:limit:{limit}"
    cached_products=await redis_client.get(cache_key)
    if cached_products:
        print("products is fetching from redis")
        return {"data from redis: ":json.loads(cached_products)}
    print("getting data from postgres sql")
    
        
    db_products=db.query(database_model.Product).offset(skip).limit(limit).all()
    product_data=[
       { 
            "id":product.id,
            "name":product.name,
            "quantity":product.quantity,
            "price":product.price,
            "category":product.category,
            "description": product.description
        }
       for product in db_products
    ]
    await redis_client.set(cache_key,
                           json.dumps(product_data),
                           ex=180
                           )
    
    return {"data from postgres":product_data}


@obj.get("/product/{id}")

async def get_product(id:int, email:str=Depends(token_verfication), db:Session=Depends(get_db)):
    cached_product=await redis_client.get(f"product:{id}")
    selected_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if cached_product:
        return {"product is cache:":json.loads(cached_product)}
    elif selected_product:
        if(selected_product):
            product_data={
                "id":selected_product.id,
                "name":selected_product.name,
                "category":selected_product.category,
                "price":selected_product.price,
                "quantity":selected_product.quantity,
                "description": selected_product.description
            }
            await redis_client.set(
                f"product:{id}",
                json.dumps(product_data),
                ex=180
            )
            return {"getting data from postgres:":product_data}
    else:    
        return "product not found"
    

@obj.post("/product")
async def app_prod(productss:Product, email:str=Depends(token_verfication),db:Session=Depends(get_db)):
    new_product=database_model.Product(**productss.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    product_data= {
        "id":new_product.id,
        "name":new_product.name,
        "quantity":new_product.quantity,
        "category":new_product.category,
        "price":new_product.price,
        "description":new_product.description
    }
    # Send background job to Redis through ARQ
    await obj.state.arq_pool.enqueue_job(
        "product_created",
        product_data
    )
    await redis_client.set(
        f"product:{product_data['id']}",
        json.dumps(product_data),
        ex=180
        )
    keys = await redis_client.keys("products:page:*")

    if keys:
        await redis_client.delete(*keys)

    return product_data
    
    
@obj.put("/product")
async def update_prod(id:int,productss:Product,email:str=Depends(token_verfication), db:Session=Depends(get_db)):
    selected_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if selected_product:
        selected_product.name=productss.name
        selected_product.category=productss.category
        selected_product.price=productss.price
        selected_product.quantity=productss.quantity
        selected_product.description=productss.description
        db.commit()
        db.refresh(selected_product)
        
        product_data= {
                "id":selected_product.id,
                "name":selected_product.name,
                "quantity":selected_product.quantity,
                "category":selected_product.category,
                "price":selected_product.price,
                "description":selected_product.description
            }
        await redis_client.set(
            f"product:{product_data['id']}",
            json.dumps(product_data),
            ex=180
            )
        keys = await redis_client.keys("products:page:*")

        if keys:
            await redis_client.delete(*keys)
        return {
            "message": "Product updated",
            "data": product_data
}
    else:
        return "product doesn't exist"        
        
    
        
        

@obj.delete("/product")
async def delete_prod(id:int,email:str=Depends(token_verfication), db:Session=Depends(get_db)):
    selected_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if selected_product:
        db.delete(selected_product)
        db.commit()
        await redis_client.delete(f"product:{id}")
        keys = await redis_client.keys("products:page:*")
        
        if keys:
            await redis_client.delete(*keys)
    
        return "Product deleted successfully"
    else:
        return "Product id not found"
        
    
        
        
    