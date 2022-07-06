from boto3 import Session
from typing import Callable
from dotenv import load_dotenv
from os import environ
environ.clear()
load_dotenv()

aws_client: Callable = Session(
    aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=environ.get('AWS_REGION_NAME')
).client

aws_resource: Callable = Session(
    aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=environ.get('AWS_REGION_NAME')
).resource


lamb = aws_client('lambda')
s3 = aws_client('s3')
api = aws_client('apigateway')
ses = aws_client('ses')
cognito = aws_client('cognito-idp')
