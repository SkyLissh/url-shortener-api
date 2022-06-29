from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


async def found_url(db: AsyncSession, *, url_key: str) -> models.URL:
    url = await crud.url.get_by_key(db, url_key=url_key)

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return url


@router.get("/", response_model=list[schemas.URL])
async def get_urls(
    *,
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> list[models.URL]:
    return await crud.url.get_all(db, skip=skip, limit=limit)


@router.get("/{url_key}", response_model=schemas.URL)
async def get_url(
    *,
    db: AsyncSession = Depends(deps.get_db),
    url_key: str,
) -> models.URL:
    url = await found_url(db, url_key=url_key)

    return url


@router.post("/", response_model=schemas.URL)
async def create_url(
    *,
    db: AsyncSession = Depends(deps.get_db),
    url_in: schemas.URLCreate,
) -> models.URL:
    target_url = await crud.url.get_by_target_url(db, target_url=url_in.target_url)

    if target_url:
        raise HTTPException(status_code=400, detail="URL already exists")

    return await crud.url.create(db, obj_in=url_in)


@router.patch("/{url_key}", response_model=schemas.URL)
async def update_url(
    *,
    db: AsyncSession = Depends(deps.get_db),
    url_key: str,
    url_in: schemas.URLUpdate,
) -> models.URL:
    url = await found_url(db, url_key=url_key)

    await crud.url.update(db, id=url.id, obj_in=url_in)

    return url


@router.delete("/{url_key}", status_code=204)
async def delete_url(
    *,
    db: AsyncSession = Depends(deps.get_db),
    url_key: str,
) -> None:
    url = await found_url(db, url_key=url_key)

    await crud.url.delete(db, id=url.id)
