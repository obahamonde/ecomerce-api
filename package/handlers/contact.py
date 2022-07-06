from dotenv import load_dotenv
from os import environ
from package.utils import id
load_dotenv()

from package.models.schemas import Contact
from package.services.fauna import Q
from package.services.aws import ses
from pydantic import EmailStr

def createContact(name:str, email:EmailStr, message:str):
    contact = Contact(name=name, email=email, message=message)
    try:
        res = Q.read("contacts", "email", contact.email)
        if res:
            Q.update("contacts", "email", contact.email, contact)
            return contact
        else:
            res = Q.create(contact)
            return contact
    except Exception:
        return None

def getContacts():
    try:
        res = Q.read_all("contacts",20)
        return res
    except Exception:
        return None

def getContact(email:EmailStr):
    try:
        res = Q.read("contacts", "email", email)
        return res
    except Exception:
        return None

def deleteContact(email:EmailStr):
    try:
        res = Q.delete("contacts", "email", email)
        return res
    except Exception:
        return None

def sendEmail(contact:Contact):
    try:
        res = ses.send_email(
            Source=environ.get('SES_FROM_EMAIL'),
            Destination={
                'ToAddresses': ['vuenyl@oscarbahamonde.cloud','dev@oscarbahamonde.cloud'],
                'CcAddresses': [contact.email]
            },
            Message={
                'Subject': {
                    'Data': f"{contact.name}<{contact.email}> sent you a message"
                },
                'Body': {
                    'Text': {
                        'Data': contact.message
                    }
                }
            })
        return res
    except Exception:
        raise Exception("Error sending email")