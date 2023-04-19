from pydantic import BaseModel


class Person(BaseModel):
    email:str
    name:str
    phone:str
    password:str


class LoginPerson(BaseModel):
    email:str
    password:str