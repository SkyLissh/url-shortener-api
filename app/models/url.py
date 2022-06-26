import secrets

from sqlalchemy import Boolean, Column, Integer, String

from app.db.base_class import Base


class URL(Base):
    url: str = Column(
        String(10), unique=True, index=True, default=secrets.token_urlsafe(7)
    )
    admin_url: str = Column(
        String(10), unique=True, index=True, default=secrets.token_urlsafe(7)
    )
    target_url: str = Column(String(255), unique=True, index=True)
    is_active: bool = Column(Boolean, default=True)
    clicks: int = Column(Integer, default=0)
