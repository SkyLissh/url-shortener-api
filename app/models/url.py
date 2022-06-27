import secrets
from typing import Callable

from sqlalchemy import Boolean, Column, Integer, String

from app.db.base_class import Base

generate_url_key: Callable[[], str] = lambda: secrets.token_urlsafe(7)


class URL(Base):
    url: str = Column(String(10), unique=True, index=True, default=generate_url_key)
    admin_url: str = Column(
        String(10), unique=True, index=True, default=generate_url_key
    )
    target_url: str = Column(String(255), unique=True, index=True)
    is_active: bool = Column(Boolean, default=True)
    clicks: int = Column(Integer, default=0)
