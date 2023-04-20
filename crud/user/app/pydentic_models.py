from pydantic import BaseModel


class Person(BaseModel):
    email:str
    name:str
    phone:str
    password:str


class LoginPerson(BaseModel):
    email:str
    password:str

class Delete(BaseModel):
    id:int

class Get_Person(BaseModel):
    id:int

class Update_Person(BaseModel):
    id:int
    email:str
    name:str
    phone:str
    password:str