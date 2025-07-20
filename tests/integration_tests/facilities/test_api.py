from httpx import AsyncClient


async def test_get_facilities(ac: AsyncClient):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
