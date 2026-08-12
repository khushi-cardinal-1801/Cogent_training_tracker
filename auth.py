from fastapi import FastAPI, HTTPException, Depends, APIRouter
from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta, datetime
from model import User
from database_model import UserDB
from passlib.hash import bcrypt
from database import session_local,base,engine
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()
   
def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()
        

router=APIRouter()
base.metadata.create_all(bind=engine)

secret_key=os.getenv("secret_key")
algorithm='HS256'
expiry_time=30



security=HTTPBearer()

def create_token(email):
    expire=datetime.now()+timedelta(minutes=expiry_time)
    payload={
        'email':email,
        'exp':expire
    }
    token=jwt.encode(payload,secret_key, algorithm=algorithm)
    return token
    
    
#signup
@router.post("/signup")
def signup(data: User, db:Session=Depends(get_db)):
    existing_user=db.query(UserDB).filter(
        UserDB.email==data.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400,
                            detail="user already exist")

    hashed_password = bcrypt.hash(data.password)

    new_user=UserDB(email=data.email,
            password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }
              
#login
@router.post('/login')
def login(data:User,db:Session=Depends(get_db)):
    
    user=db.query(UserDB).filter(UserDB.email==data.email).first()
    if user:
        if(bcrypt.verify(data.password,user.password)):
            token_create=create_token(data.email)
            return {"access_token": token_create,
                    "token_type":"bearer"}
        raise HTTPException(status_code=401,
                            detail="Invalid Password")
    raise HTTPException(status_code=404,
                        detail="Invalid credentials")
    
#token verification

def token_verfication(credentials:HTTPAuthorizationCredentials = Depends(security) ):
    token=credentials.credentials
    try:
        payload=jwt.decode(token, secret_key, algorithms=[algorithm])
        email=payload.get('email')
        return email
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="decoded token didnt match")
    
    
@router.get("/profile")
def profile(email:str=Depends(token_verfication)):
    return {"hello email":email}