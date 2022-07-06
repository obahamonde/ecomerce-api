from dotenv import load_dotenv
from os import environ
load_dotenv()

from package.handlers.bucket import create_archive
from package.handlers.user import access_token, getUser, globalLogout, putUser, getUid 
from package.models.schemas import User
from package.services.fauna import Q
from fastapi import APIRouter, UploadFile, File, Request, Response, status, HTTPException, Depends
from starlette.responses import JSONResponse, RedirectResponse

user = APIRouter()

def get_uid(token:str)->str:
    res = getUser(token)
    return res['uid']

@user.get('/auth')
async def auth(code: str):
    token = access_token(code)
    return RedirectResponse(url=f"http://localhost:3333/auth?token={token}")

@user.post('/user')
async def create_user(token:str):
    response = getUser(token)
    return response

@user.put('/user/avatar')
async def update_user(uid:str = Depends(getUid), avatar: UploadFile = File(...)):
    archive = create_archive(uid, avatar)
    user = putUser(uid, archive.url)
    return user

@user.get('/logout')        
async def logout(token:str):
    response = globalLogout(token)
    return response.json()

    