from dotenv import load_dotenv
from os import environ
load_dotenv()

from pydantic import HttpUrl, EmailStr

from package.services.aws import cognito, ses
from package.services.fauna import Q
from package.models.schemas import User, Contact
from requests import post
from package.utils import avatar

def getPayload(code:str)->str:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': environ.get('COGNITO_CLIENT_ID'),
        'client_secret': environ.get('COGNITO_CLIENT_SECRET'),
        'code': code,
        'redirect_uri': environ.get('COGNITO_REDIRECT_URI')
    }
    response = post(f"{environ.get('COGNITO_URL')}/oauth2/token", headers=headers, data=data)
    return response.json()

def access_token(code:str)->str:
    payload = getPayload(code)
    return payload['access_token']

def getUser(token:str)->User:
    response = cognito.get_user(AccessToken=token)
    user = User(
        uid=response['UserAttributes'][0]['Value'],
        email=response['UserAttributes'][2]['Value'],
        name=response['Username'],
        avatar=avatar())
    try:
        Q.create(user)
        return user
    except Exception:
        return Q.read("user", "uid", user.uid)
        
        

def getUid(token:str)->str:
    res = getUser(token)
    return res.uid

def putUser(uid:str, avatar:HttpUrl):
    try:
        user = Q.read("user", "uid", uid)
        user.avatar = avatar
        Q.update("user", "uid", uid , user)
        return user
    except Exception:
        return None

def refreshAuth(refresh_token:str)->str:
    response = cognito.initiate_auth(
        AuthFlow='REFRESH_TOKEN',
        ClientId=environ.get('COGNITO_CLIENT_ID'),
        AuthParameters={
            'REFRESH_TOKEN': refresh_token
        }
    )
    token = response['AuthenticationResult']['AccessToken']
    return token

def globalLogout(token:str)->str:
    response = cognito.global_sign_out(AccessToken=token)
    return response['GlobalSignOutResponse']['Message']