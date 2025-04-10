import pytest
from datetime import datetime, timedelta
from app.models.table import Table
from app.models.reservation import Reservation

def test_create_reservation(client, db_session):
    # Создаем тестовый стол
    table = Table(name="Тестовый стол", seats=4, location="Тестовый зал")
    db_session.add(table)
    db_session.commit()

    # Создаем бронирование
    reservation_time = datetime.now() + timedelta(hours=1)
    response = client.post(
        "/api/reservations",
        json={
            "customer_name": "Иван Иванов",
            "table_id": table.id,
            "reservation_time": reservation_time.isoformat(),
            "duration_minutes": 120
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Иван Иванов"
    assert data["table_id"] == table.id
    assert data["duration_minutes"] == 120

def test_get_reservations(client, db_session):
    # Создаем тестовый стол и бронирование
    table = Table(name="Тестовый стол", seats=4, location="Тестовый зал")
    db_session.add(table)
    db_session.commit()

    reservation = Reservation(
        customer_name="Иван Иванов",
        table_id=table.id,
        reservation_time=datetime.now() + timedelta(hours=1),
        duration_minutes=120
    )
    db_session.add(reservation)
    db_session.commit()

    response = client.get("/api/reservations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["customer_name"] == "Иван Иванов"

def test_get_reservation(client, db_session):
    # Создаем тестовый стол и бронирование
    table = Table(name="Тестовый стол", seats=4, location="Тестовый зал")
    db_session.add(table)
    db_session.commit()

    reservation = Reservation(
        customer_name="Иван Иванов",
        table_id=table.id,
        reservation_time=datetime.now() + timedelta(hours=1),
        duration_minutes=120
    )
    db_session.add(reservation)
    db_session.commit()

    response = client.get(f"/api/reservations/{reservation.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "Иван Иванов"
    assert data["id"] == reservation.id

def test_update_reservation(client, db_session):
    # Создаем тестовый стол и бронирование
    table = Table(name="Тестовый стол", seats=4, location="Тестовый зал")
    db_session.add(table)
    db_session.commit()

    reservation = Reservation(
        customer_name="Иван Иванов",
        table_id=table.id,
        reservation_time=datetime.now() + timedelta(hours=1),
        duration_minutes=120
    )
    db_session.add(reservation)
    db_session.commit()

    new_time = datetime.now() + timedelta(hours=2)
    response = client.put(
        f"/api/reservations/{reservation.id}",
        json={
            "customer_name": "Петр Петров",
            "reservation_time": new_time.isoformat(),
            "duration_minutes": 180
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "Петр Петров"
    assert data["duration_minutes"] == 180

def test_delete_reservation(client, db_session):
    # Создаем тестовый стол и бронирование
    table = Table(name="Тестовый стол", seats=4, location="Тестовый зал")
    db_session.add(table)
    db_session.commit()

    reservation = Reservation(
        customer_name="Иван Иванов",
        table_id=table.id,
        reservation_time=datetime.now() + timedelta(hours=1),
        duration_minutes=120
    )
    db_session.add(reservation)
    db_session.commit()

    response = client.delete(f"/api/reservations/{reservation.id}")
    assert response.status_code == 204

    # Проверяем, что бронирование удалено
    response = client.get(f"/api/reservations/{reservation.id}")
    assert response.status_code == 404

def test_reservation_validation(client, db_session):
    # Создаем тестовый стол
    table = Table(name="Тестовый стол", seats=4, location="Тестовый зал")
    db_session.add(table)
    db_session.commit()

    # Проверка валидации времени в прошлом
    past_time = datetime.now() - timedelta(hours=1)
    response = client.post(
        "/api/reservations",
        json={
            "customer_name": "Иван Иванов",
            "table_id": table.id,
            "reservation_time": past_time.isoformat(),
            "duration_minutes": 120
        }
    )
    assert response.status_code == 422

    # Проверка валидации слишком короткой длительности
    response = client.post(
        "/api/reservations",
        json={
            "customer_name": "Иван Иванов",
            "table_id": table.id,
            "reservation_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "duration_minutes": 20
        }
    )
    assert response.status_code == 422

    # Проверка валидации слишком длительной брони
    response = client.post(
        "/api/reservations",
        json={
            "customer_name": "Иван Иванов",
            "table_id": table.id,
            "reservation_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "duration_minutes": 300
        }
    )
    assert response.status_code == 422

def test_reservation_conflict(client, db_session):
    # Создаем тестовый стол
    table = Table(name="Тестовый стол", seats=4, location="Тестовый зал")
    db_session.add(table)
    db_session.commit()

    # Создаем первое бронирование
    reservation_time = datetime.now() + timedelta(hours=1)
    response = client.post(
        "/api/reservations",
        json={
            "customer_name": "Иван Иванов",
            "table_id": table.id,
            "reservation_time": reservation_time.isoformat(),
            "duration_minutes": 120
        }
    )
    assert response.status_code == 201

    # Пытаемся создать конфликтующее бронирование
    response = client.post(
        "/api/reservations",
        json={
            "customer_name": "Петр Петров",
            "table_id": table.id,
            "reservation_time": (reservation_time + timedelta(minutes=30)).isoformat(),
            "duration_minutes": 120
        }
    )
    assert response.status_code == 409 