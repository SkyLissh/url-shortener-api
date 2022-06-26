from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_base import CrudBase
from app.models.url import URL
from app.schemas.url import URLCreate, URLUpdate


class CrudURL(CrudBase[URL, URLCreate, URLUpdate]):
    async def get_by_key(self, db: AsyncSession, *, url_key: str) -> URL | None:
        select_query = select([self.model]).where(self.model.url == url_key)
        result = await db.execute(select_query)

        return cast(URL | None, result.scalar())

    async def get_by_target_url(
        self, db: AsyncSession, *, target_url: str
    ) -> URL | None:
        select_query = select([self.model]).where(self.model.target_url == target_url)
        result = await db.execute(select_query)

        return cast(URL | None, result.scalar())


url = CrudURL(URL)
