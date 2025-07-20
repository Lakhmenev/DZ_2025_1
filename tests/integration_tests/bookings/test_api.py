import pytest
from httpx import AsyncClient

from src.utils.db_manager import DBManager


async def test_add_booking(db: DBManager, authenticated_ac: AsyncClient):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2024-08-01",
            "date_to": "2024-08-10",
        })
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    assert "data" in res
