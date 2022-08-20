from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.api.api_v1 import api
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/{settings.API_URL}/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(api.api_router, prefix=f"/{settings.API_URL}")
if settings.IS_PRODUCTION:
    app.docs_url = None
    app.redoc_url = f"/{settings.BASE_URL}/"

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
