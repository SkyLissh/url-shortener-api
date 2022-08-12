from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.api.api_v1.endpoints import hello, url

api_router = APIRouter(default_response_class=ORJSONResponse)

api_router.include_router(hello.router, tags=["Hello"])
api_router.include_router(url.router, prefix="/url", tags=["Url"])
