from package.models.schemas import Vinyl
from package.services.fauna import Q
from fastapi import APIRouter, HTTPException, Response, status
from starlette.responses import JSONResponse


vinyl = APIRouter()

@vinyl.get("/vinyls")
async def get_vinyls():
    """
    Get all vinyls
    """
    vinyls = Q.read_all("vinyl", 64)
    return JSONResponse(vinyls, status_code=status.HTTP_200_OK)

