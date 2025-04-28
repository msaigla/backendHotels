import json
import pytest

from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def create_hotels(setup_database):
    with open('tests/mock_hotels.json', 'r') as json_file:
        json_data = json.load(json_file)
        for hotel in json_data:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                await ac.post(
                    "/hotels",
                    json=hotel
                )


@pytest.fixture(scope="session", autouse=True)
async def create_rooms(create_hotels):
    with open('tests/mock_rooms.json', 'r') as json_file:
        json_data = json.load(json_file)
        for room in json_data:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                print(room)
                await ac.post(
                    f"/rooms/{room['hotel_id']}/rooms",
                    json={
                        "title": room["title"],
                        "description": room["description"],
                        "price": room["price"],
                        "quantity": room["quantity"],
                        "facilities_ids": []
                    }
                )


@pytest.fixture(scope="session", autouse=True)
async def register_user(create_rooms):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "test@test.ru",
                "password": "1234"
            }
        )
