from package.handlers.contact import  sendEmail
from package.services.fauna import Q
from package.models.schemas import Contact
from fastapi import APIRouter, Request, status, HTTPException
from starlette.responses import JSONResponse

contact = APIRouter()

@contact.post('/')
async def send_email(name: str, email: str, message: str):
    """
    Send email to admin
    """
    contact = Contact(name=name, email=email, message=message)
    await sendEmail(contact)
    return JSONResponse(status_code=status.HTTP_200_OK)