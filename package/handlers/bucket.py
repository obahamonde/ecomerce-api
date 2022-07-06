from dotenv import load_dotenv
from os import environ
from package.utils import id
load_dotenv()

from package.services.aws import s3
from package.services.fauna import Q
from package.models.schemas import Archive
from fastapi import UploadFile, File
from typing import List

def create_archive(uid:str, file: UploadFile = File(...)):
    i = id()
    dictionary = {
        "mid": i,
        "uid": uid,
        "name": file.filename,
        "content_type": file.content_type,
        "url": f"http://{environ.get('S3_BUCKET')}.s3.amazonaws.com/{uid}/{i}/{file.filename}"
    }
    Q.create(Archive(**dictionary))
    s3.upload_file(file.file, environ.get('S3_BUCKET'), f"{uid}/{i}/{file.filename}")
    return Archive(**dictionary)

def get_archive(mid: str) -> Archive:
    return Q.read("archives", "mid", id)

def get_all_archives() -> List[Archive]:
    return Q.read_all("archives", 20)

def delete_archive(mid: str) -> Archive:
    return Q.delete("archives", "mid", id)