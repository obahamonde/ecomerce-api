from pydantic import BaseModel, HttpUrl, EmailStr, Field, BaseConfig
from fastapi import UploadFile, File
from typing import Optional, List, Dict, Union, Callable
from package.utils import id, avatar

class User(BaseModel):
    uid:str = Field(...)
    name:str = Field(...)
    email:EmailStr = Field(...)
    avatar:HttpUrl = Field(default_factory=avatar)

class Contact(BaseModel):
    uid:str = Field(default_factory=id)
    name:str = Field(...)
    email:EmailStr = Field(...)
    message:str = Field(...)
    isAdmin:bool = Field(default=False)

class Archive(BaseModel):
    mid:str = Field(default_factory=id)
    uid:str = Field(...)
    name:str = Field(...)
    url:Optional[HttpUrl] = Field()
    content_type:str = Field(...)

class Product(BaseModel):
    pid:str = Field(default_factory=id)
    name:str = Field(...)
    title:str = Field(...)
    description:str = Field(...)
    price:float = Field(...)
    archives:List[Archive] = Field(default_factory=list)
    category:str = Field(...)
    tags:List[str] = Field(default_factory=list)
    stock:int = Field(...)
    delivery_time:str = Field(...)
    class Config(BaseConfig):
            arbitrary_types_allowed: bool = True

class Order(BaseModel):
    oid:str = Field(default_factory=id)
    product:Product = Field(...)
    user:User = Field(...)
    quantity:int = Field(...)
    price:float = Field(...)
    status:str = Field(default="pending")
    class Config(BaseConfig):
        arbitrary_types_allowed: bool = True

class Vinyl(BaseModel):
        img: Optional[str]
        title: Optional[str]
        price: Optional[str]
        category: Optional[str]
        url: Optional[str]