from pydantic import BaseModel
from typing import List, Optional


class Blog(BaseModel):
    title: str
    body: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str]=None    


class User(BaseModel):
    name: str
    email:str
    password:str

class Show_user(BaseModel):
    name: str
    email:str
class Login(BaseModel):
    username: str
    password: str
