from fastapi import FastAPI, HTTPException, Depends
from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta, datetime
from model import User
from passlib.hash import bcrypt
    

obj=FastAPI()
users=[]
print(users)

secret_key='khushi aggarwal'
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
@obj.post("/signup")
def signup(data: User):

    for user in users:

        if user["email"] == data.email:
            raise HTTPException(
                status_code=400,
                detail="User already exists"
            )

    hashed_password = bcrypt.hash(data.password)

    users.append({
        "email": data.email,
        "password": hashed_password
    })

    return {
        "message": "User registered successfully"
    }
              
#login
@obj.post('/login')
def login(data:User):
    for user in users:
        if(data.email==user['email']):
            if(bcrypt.verify(data.password, user['password'])):
                token=create_token(data.email)
                return {"access token=":token,
                        "token type":"bearer"}
            raise HTTPException(status_code=404,detail="Invalid password")

    raise HTTPException(status_code=404, detail="Invalid credentials, please enter the correct one ")

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
    
    
@obj.get("/profile")
def profile(email:str=Depends(token_verfication)):
    return {"hello email":email}