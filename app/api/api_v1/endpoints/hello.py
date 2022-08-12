from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

router = APIRouter(default_response_class=ORJSONResponse)


@router.get("/")
async def get() -> dict[str, str]:
    return {"message": "Hello World!"}
