from fastapi import APIRouter, UploadFile, File, Request, status, Depends
from package.handlers.bucket import create_archive, get_archive, get_all_archives, delete_archive
from starlette.responses import JSONResponse
from package.handlers.user import getUid

bucket = APIRouter()

@bucket.post('/uploads')
async def upload(uid: str = Depends(getUid), file: UploadFile = File(...)):
    archive = create_archive(uid, file)
    return archive

@bucket.get('/uploads')
async def get_all_uploads(uid: str = Depends(getUid)):
    archives = get_all_archives(uid)
    return archives

@bucket.delete('/uploads/{mid}')
async def delete_upload(mid: str, uid: str = Depends(getUid)):
    archive = delete_archive(uid, mid)
    return archive