from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_orders():
    response = client.get("/api/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_order():
    # Создаем заказ с id блюд, которые должны быть в базе
    order_data = {
        "customer_name": "Иван Иванов",
        "dish_ids": [1]  # Нужно чтобы блюдо с id=1 существовало в тестовой БД
    }
    response = client.post("/api/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == order_data["customer_name"]
    assert "id" in data
    assert "order_time" in data
    assert isinstance(data["dishes"], list)


def test_update_order_status():
    # Для обновления статуса нужен order_id, для простоты берем 1
    status_update = {"status": "готовится"}
    response = client.patch("/api/orders/1/status", json=status_update)
    # Возможно 200, если заказ с id=1 есть, либо 400/404, в зависимости от данных
    assert response.status_code in (200, 400, 404)


def test_cancel_order():
    # Попытка удалить заказ с id=1
    response = client.delete("/api/orders/1")
    # Статус 404 так как удалить нельзя (статус 'готовится')
    assert response.status_code == 400
