import json
from typing import TypedDict
from uuid import UUID

from httpx import AsyncClient
from pytest import MonkeyPatch
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.core.config import settings

# === MODELS ===


class URLRequest(TypedDict):
    target_url: str


class URL(URLRequest):
    id: str
    url: str
    clicks: int
    is_active: bool


# === READ ===


async def test_read_all_urls(client: AsyncClient, monkeypatch: MonkeyPatch) -> None:
    test_data: list[URL] = [
        {
            "id": "0c0bf3d9-f66d-4f4c-831f-e7794db32028",
            "target_url": "http://example.com",
            "url": "ASthsFTYQQ",
            "clicks": 0,
            "is_active": True,
        },
        {
            "id": "d09edf35-e59c-4f7f-a24c-a4a9a74b9595",
            "target_url": "http://another.com",
            "url": "mOF7jczI0Q",
            "clicks": 0,
            "is_active": True,
        },
    ]

    async def mock_get_all(db: AsyncSession, skip: int, limit: int) -> list[URL]:
        return test_data

    monkeypatch.setattr(crud.url, "get_all", mock_get_all)

    response = await client.get("/url/")
    assert response.status_code == 200
    assert response.json() == test_data


async def test_read_url(client: AsyncClient, monkeypatch: MonkeyPatch) -> None:
    test_data: URL = {
        "id": "0c0bf3d9-f66d-4f4c-831f-e7794db32028",
        "target_url": "http://example.com",
        "url": "ASthsFTYQQ",
        "clicks": 0,
        "is_active": True,
    }

    async def mock_get_by_key(db: AsyncSession, url_key: str) -> URL:
        return test_data

    monkeypatch.setattr(crud.url, "get_by_key", mock_get_by_key)

    response = await client.get("/url/ASthsFTYQQ")
    assert response.status_code == 200
    assert response.json() == test_data


async def test_read_url_not_found(
    client: AsyncClient, monkeypatch: MonkeyPatch
) -> None:
    async def mock_get_by_key(db: AsyncSession, url_key: str) -> None:
        return None

    monkeypatch.setattr(crud.url, "get_by_key", mock_get_by_key)

    response = await client.get("/url/ASthsFTYQQ")
    assert response.status_code == 404
    assert response.json() == {"detail": "URL not found"}


# === CREATE ===


async def create_url(client: AsyncClient, monkeypatch: MonkeyPatch) -> None:
    test_request: URLRequest = {
        "target_url": "http://example.com",
    }
    test_response: URL = {
        "id": "0c0bf3d9-f66d-4f4c-831f-e7794db32028",
        "target_url": "http://example.com",
        "url": "ASthsFTYQQ",
        "clicks": 0,
        "is_active": True,
    }

    async def mock_create(db: AsyncSession, obj_in: URL) -> str:
        return "ASthsFTYQQ"

    monkeypatch.setattr(crud.url, "create", mock_create)

    response = await client.post("/url/", json=test_request)
    assert response.status_code == 201
    assert response.json() == test_response


async def test_create_url_already_exists(
    client: AsyncClient, monkeypatch: MonkeyPatch
) -> None:
    test_request: URLRequest = {
        "target_url": "http://example.com",
    }

    test_data: URL = {
        "id": "0c0bf3d9-f66d-4f4c-831f-e7794db32028",
        "target_url": "http://example.com",
        "url": "ASthsFTYQQ",
        "clicks": 0,
        "is_active": True,
    }

    async def mock_create(db: AsyncSession, target_url: str) -> URL:
        return test_data

    monkeypatch.setattr(crud.url, "get_by_target_url", mock_create)

    response = await client.post("/url/", json=test_request)
    assert response.status_code == 200
    assert response.json() == test_data


async def test_create_url_recursive(
    client: AsyncClient, monkeypatch: MonkeyPatch
) -> None:
    test_request: URLRequest = {
        "target_url": "http://example.com",
    }

    monkeypatch.setattr(settings, "BACKEND_CORS_ORIGINS", ["http://example.com"])

    response = await client.post("/url/", json=test_request)
    assert response.status_code == 400
    assert response.json() == {"detail": "This URL is not allowed to be shortened"}


# === UPDATE ===
async def test_update_url(client: AsyncClient, monkeypatch: MonkeyPatch) -> None:
    test_request: URLRequest = {
        "target_url": "http://example.com",
    }
    test_data = schemas.URL(
        id="0c0bf3d9-f66d-4f4c-831f-e7794db32028",
        target_url="http://example.com",
        url="ASthsFTYQQ",
        clicks=0,
        is_active=True,
    )

    async def mock_get_by_key(db: AsyncSession, url_key: str) -> schemas.URL:
        return test_data

    monkeypatch.setattr(crud.url, "get_by_key", mock_get_by_key)

    async def mock_update(db: AsyncSession, id: UUID, obj_in: URL) -> None:
        return None

    monkeypatch.setattr(crud.url, "update", mock_update)

    response = await client.patch("/url/ASthsFTYQQ", json=test_request)
    assert response.status_code == 200
    assert response.json() == json.loads(test_data.json())


async def test_update_url_not_found(
    client: AsyncClient, monkeypatch: MonkeyPatch
) -> None:
    test_request: URLRequest = {
        "target_url": "http://example.com",
    }

    async def mock_get_by_key(db: AsyncSession, url_key: str) -> None:
        return None

    monkeypatch.setattr(crud.url, "get_by_key", mock_get_by_key)

    response = await client.patch("/url/ASthsFTYQQ", json=test_request)
    assert response.status_code == 404
    assert response.json() == {"detail": "URL not found"}


# === DELETE ===


async def test_delete_url(client: AsyncClient, monkeypatch: MonkeyPatch) -> None:
    test_data = schemas.URL(
        id="0c0bf3d9-f66d-4f4c-831f-e7794db32028",
        target_url="http://example.com",
        url="ASthsFTYQQ",
        clicks=0,
        is_active=True,
    )

    async def mock_get_by_key(db: AsyncSession, url_key: str) -> schemas.URL:
        return test_data

    monkeypatch.setattr(crud.url, "get_by_key", mock_get_by_key)

    async def mock_delete(db: AsyncSession, id: UUID) -> None:
        return None

    monkeypatch.setattr(crud.url, "delete", mock_delete)

    response = await client.delete("/url/ASthsFTYQQ")
    assert response.status_code == 204


async def test_delete_url_not_found(
    client: AsyncClient, monkeypatch: MonkeyPatch
) -> None:
    async def mock_get_by_key(db: AsyncSession, url_key: str) -> None:
        return None

    monkeypatch.setattr(crud.url, "get_by_key", mock_get_by_key)

    response = await client.delete("/url/ASthsFTYQQ")
    assert response.status_code == 404
    assert response.json() == {"detail": "URL not found"}
