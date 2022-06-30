from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    HTTPX client for testing.
    """

    async with AsyncClient(app=app, base_url="http://test/api/v1") as client:
        yield client
