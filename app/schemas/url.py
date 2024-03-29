from datetime import datetime
from uuid import UUID

from pydantic import HttpUrl

from app.schemas.base import Base


class URLBase(Base):
    target_url: HttpUrl | None


class URLCreate(URLBase):
    target_url: HttpUrl


class URLUpdate(URLBase):
    clicks: int | None
    is_active: bool | None


class URLInDBBase(URLBase):
    id: UUID
    clicks: int
    is_active: bool
    url: str

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class URLInDB(URLInDBBase):
    admin_url: str


class URL(URLInDBBase):
    pass
