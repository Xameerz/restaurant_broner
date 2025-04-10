import pytest
from datetime import datetime
from app.models.table import Table

def test_create_table(client):
    response = client.post(
        "/api/tables",
        json={
            "name": "Стол у окна",
            "seats": 4,
            "location": "Зал 1"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Стол у окна"
    assert data["seats"] == 4
    assert data["location"] == "Зал 1"
    assert "id" in data

def test_get_tables(client, db_session):
    # Создаем тестовый стол
    table = Table(name="Тестовый стол", seats=2, location="Тестовый зал")
    db_session.add(table)
    db_session.commit()

    response = client.get("/api/tables")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Тестовый стол"

def test_get_table(client, db_session):
    # Создаем тестовый стол
    table = Table(name="Тестовый стол", seats=2, location="Тестовый зал")
    db_session.add(table)
    db_session.commit()

    response = client.get(f"/api/tables/{table.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Тестовый стол"
    assert data["id"] == table.id

def test_update_table(client, db_session):
    # Создаем тестовый стол
    table = Table(name="Тестовый стол", seats=2, location="Тестовый зал")
    db_session.add(table)
    db_session.commit()

    response = client.put(
        f"/api/tables/{table.id}",
        json={
            "name": "Обновленный стол",
            "seats": 4,
            "location": "Новый зал"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Обновленный стол"
    assert data["seats"] == 4
    assert data["location"] == "Новый зал"

def test_delete_table(client, db_session):
    # Создаем тестовый стол
    table = Table(name="Тестовый стол", seats=2, location="Тестовый зал")
    db_session.add(table)
    db_session.commit()

    response = client.delete(f"/api/tables/{table.id}")
    assert response.status_code == 204

    # Проверяем, что стол удален
    response = client.get(f"/api/tables/{table.id}")
    assert response.status_code == 404

def test_create_table_validation(client):
    # Проверка валидации минимального количества мест
    response = client.post(
        "/api/tables",
        json={
            "name": "Стол",
            "seats": 0,
            "location": "Зал"
        }
    )
    assert response.status_code == 422

    # Проверка валидации максимального количества мест
    response = client.post(
        "/api/tables",
        json={
            "name": "Стол",
            "seats": 21,
            "location": "Зал"
        }
    )
    assert response.status_code == 422

    # Проверка валидации пустого названия
    response = client.post(
        "/api/tables",
        json={
            "name": "",
            "seats": 4,
            "location": "Зал"
        }
    )
    assert response.status_code == 422 