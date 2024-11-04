from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Тест для POST-запроса /calculate/
def test_calculate_addition():
    response = client.post("/calculate/", json={"num1": 10, "num2": 5, "operation": "add"})
    assert response.status_code == 200
    assert response.json()["entry"]["result"] == 15


def test_calculate_subtraction():
    response = client.post("/calculate/", json={"num1": 15, "num2": 5, "operation": "subtract"})
    assert response.status_code == 200
    assert response.json()["entry"]["result"] == 10


def test_calculate_division_by_zero():
    response = client.post("/calculate/", json={"num1": 10, "num2": 0, "operation": "divide"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Деление на ноль недопустимо."


def test_calculate_invalid_operation():
    response = client.post("/calculate/", json={"num1": 10, "num2": 5, "operation": "invalid"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Неверная операция. Доступны: add, subtract, multiply, divide."


# Тест для GET-запроса /operations/
def test_get_operations():
    response = client.get("/operations/")
    assert response.status_code == 200
    assert "operations" in response.json()


# Тест для DELETE-запроса /operations/{operation_id}
def test_delete_operation():
    # Добавляем запись для удаления
    client.post("/calculate/", json={"num1": 20, "num2": 10, "operation": "subtract"})

    # Удаляем запись с ID 0
    response = client.delete("/operations/0")
    assert response.status_code == 200
    assert response.json()["message"] == "Запись успешно удалена"


def test_delete_nonexistent_operation():
    response = client.delete("/operations/100")
    assert response.status_code == 404
    assert response.json()["detail"] == "Запись с указанным ID не найдена"
