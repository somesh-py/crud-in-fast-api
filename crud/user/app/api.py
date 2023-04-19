from fastapi import APIRouter,Request,Form,status
from fastapi.responses import HTMLResponse,RedirectResponse
from passlib.context import CryptContext
from .models import User
import passlib
from fastapi_login import LoginManager
from .pydentic_models import Person,LoginPerson

SECRET='your-secret-key'

app=APIRouter()
manager=LoginManager(SECRET,token_url='/auth/token')
pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/registration_api/")
async def registration(data:Person):
    if await User.exists(phone=data.phone):
        return {"status":False,"messages":"phone number already exists"}
    
    elif await User.exists(email=data.email):
        return {"status":False,"messages":"email already exists"}
    
    else:
        user_obj=await User.create(emai=data.email,name=data.name,phone=data.phone,password=get_password_hash(data.password))
        return user_obj