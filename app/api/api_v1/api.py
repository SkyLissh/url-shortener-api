from fastapi import APIRouter

from app.api.api_v1.endpoints import hello, url

api_router = APIRouter()

api_router.include_router(hello.router, tags=["Hello"])
api_router.include_router(url.router, prefix="/url", tags=["Url"])
