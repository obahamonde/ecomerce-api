from fastapi import FastAPI
from package.router.user import user
from package.router.contact import contact
from package.router.bucket import bucket
from package.router.vinyls import vinyl
from fastapi.middleware.cors import CORSMiddleware

def main():
    app =FastAPI(
        title="E-commerce API",
        description="This is a cloud native e-commerce API",
        version="0.0.1",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )   
    app.include_router(user)
    app.include_router(contact)
    app.include_router(bucket)
    app.include_router(vinyl)
    return app