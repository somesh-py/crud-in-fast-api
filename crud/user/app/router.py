from fastapi import APIRouter,Request,Form,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from .models import User
import passlib
from passlib.context import CryptContext
from fastapi_login import LoginManager


router=APIRouter()

SECRET='your-secret-key'
manager=LoginManager(SECRET,token_url='/auth/token')
templates=Jinja2Templates(directory="app/templates")
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def verify_password(plain_password,hashed_password):
     return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
     return pwd_context.hash(password)

@router.get("/update/")
async def read_item(request:Request):
     return templates.TemplateResponse("update.html",{'request':request})

@router.get("/login/",response_class=HTMLResponse)
async def read_item(request:Request):
     return templates.TemplateResponse("login.html",{'request':request})

@router.get("/",response_class=HTMLResponse)
async def read_item(request:Request):
    return templates.TemplateResponse("signup.html",{"request":request})

@router.post("/registration/",response_class=HTMLResponse)
async def read_item(request:Request,Name:str=Form(...),
                    Email:str=Form(...),
                    Phone:str=Form(...),
                    Password:str=Form(...)):
    
        if await User.filter(email=Email).exists():
            return RedirectResponse("/",status_code=status.HTTP_302_FOUND)
        
        elif await User.filter(phone=Phone).exists():
             return RedirectResponse("/",status_code=status.HTTP_302_FOUND)
        else:
            user_obj= await User.create(email=Email,name=Name,phone=Phone,password=get_password_hash(Password))
            return RedirectResponse("/login/",status_code=status.HTTP_302_FOUND)



# @manager.user_loader()
# async def load_user(email:str):
#      if await User.exists(email=email):
#         user=await User.get(email=email)
#         return user

# @router.post('/loginuser/')
# async def login(request:Request,email:str=Form(...),
#                 password:str=Form(...)):
#         email=email
#         user= await load_user(email)
#         if not user:
#              return {'USER NOT REGISTERED'}
#         elif not verify_password(password,user.password):
#              return {'PASSWORD IS WRONG'}
        
#         access_token=manager.create_access_token(
#              data=dict(sub=email)
#         )

#         if "_messages" not in request.session:
#             request.session['_messages']=[]
#             new_dict={'user_id':str(user.id),"email":email,"access_token":str(access_token)}
#             request.session['_messages'].append(
#                  new_dict
#             )
#         return RedirectResponse("/update/",status_code=status.HTTP_302_FOUND)

@router.post("/logindata/",response_class=HTMLResponse)
async def login_user(request:Request,Email:str=Form(...),
                     Password:str=Form(...)):
     if await User.exists(email=Email):
          data=await User.get(email=Email)
          passwword1=data.password
          temppassword=get_password_hash(Password)
          
          def verify_password(plain_password,hashed_password):
               return pwd_context.verify(plain_password,hashed_password)
          
          if verify_password(Password,passwword1):
               print("password not matched")
               return templates.TemplateResponse("update.html",{'request':request})
          else:
               print("password incorrect")
               return templates.TemplateResponse("login.html",{'request':request,"messages":"password was incorrect"})
               
     else:
           print("email incorrect")
           return templates.TemplateResponse("login.html",{'request':request,"messages":"email was incorrect"})
