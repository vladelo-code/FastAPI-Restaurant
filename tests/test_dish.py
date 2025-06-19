import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_get_dishes():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/dishes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_create_dish():
    new_dish = {
        "name": "Борщ",
        "description": "Классический украинский суп",
        "price": 7.99,
        "category": "Основные блюда"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/dishes/", json=new_dish)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_dish["name"]
    assert data["category"] == new_dish["category"]


@pytest.mark.anyio
async def test_delete_dish():
    new_dish = {
        "name": "Пельмени",
        "description": "Русские вареники с мясом",
        "price": 5.50,
        "category": "Основные блюда"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_resp = await ac.post("/dishes/", json=new_dish)
        assert create_resp.status_code == 200
        dish_id = create_resp.json()["id"]

        delete_resp = await ac.delete(f"/dishes/{dish_id}")
        assert delete_resp.status_code == 200
        assert delete_resp.json() == {"detail": "Блюдо удалено"}

        delete_resp_again = await ac.delete(f"/dishes/{dish_id}")
        assert delete_resp_again.status_code == 404
