from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from passlib.context import CryptContext
from .models import User
import passlib
from fastapi_login import LoginManager
from .pydentic_models import Person, LoginPerson, Delete, Get_Person, Update_Person

SECRET = 'your-secret-key'

app = APIRouter()
manager = LoginManager(SECRET, token_url='/auth/token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@app.post("/registration_api/")
async def registration(data: Person):
    if await User.exists(phone=data.phone):
        return {"status": False, "messages": "phone number already exists"}

    elif await User.exists(email=data.email):
        return {"status": False, "messages": "email already exists"}

    else:
        user_obj = await User.create(email=data.email, name=data.name,
                                     phone=data.phone,
                                     password=get_password_hash(data.password))
        return user_obj


@app.post("/data/{id}")
async def all_user(data: Get_Person):
    if data.id != 0:
        user = await User.get(id=data.id)
        return user
    else:
        user = await User.all()
        return user

# @app.post("/data/{id}")
# async def get_one_user(data:Get_Person):
#     user= await User.get(id=data.id)
#     return user


@app.put("/update/{id}")
async def update(data: Update_Person):
    id = data.id
    user = await User.filter(id=id).update(id=id, email=data.email, name=data.name, phone=data.phone, password=data.password)
    return user


@app.delete("/delete_user/{id}")
async def delete(data: Delete):
    if data.id == 0 or data.id == None or data.id == " ":
        user = await User.all().delete()
        return {"status": True, "messages": "all data deleted"}
    else:
        user_obj = await User.get(id=data.id).delete()
        return {"status": True, "messages": "user delete"}
