import pytest
from fastapi.testclient import TestClient
from auth import create_access_token
import database
from main import app


@pytest.fixture
def client(tmp_path):

    test_db_path = tmp_path / "test_erp.db"

    database.set_database_path(str(test_db_path))
    database.create_tables()

    test_client = TestClient(app)

    token = create_access_token("test_user")

    test_client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    yield test_client

    database.DATABASE_PATH = "erp.db"


def test_get_equipment(client):

    response = client.get("/equipment")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_customer(client):

    response = client.post(
        "/customers",
        json={
            "id": 100,
            "name": "Test Construction",
            "phone": "9999999999",
            "email": "test@example.com"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 100
    assert data["name"] == "Test Construction"


def test_create_customer_duplicate(client):

    client.post(
        "/customers",
        json={
            "id": 101,
            "name": "Duplicate Test",
            "phone": "9999999999",
            "email": "duplicate@example.com"
        }
    )

    response = client.post(
        "/customers",
        json={
            "id": 101,
            "name": "Duplicate Test",
            "phone": "9999999999",
            "email": "duplicate@example.com"
        }
    )

    assert response.status_code == 409

def test_create_rental_and_return(client):

    # Create customer
    customer_response = client.post(
        "/customers",
        json={
            "id": 200,
            "name": "Rental Test Company",
            "phone": "8888888888",
            "email": "rental@test.com"
        }
    )

    assert customer_response.status_code == 201

    # Create equipment
    equipment_response = client.post(
        "/equipment",
        json={
            "id": 200,
            "name": "Test Excavator",
            "equipment_type": "Excavator",
            "daily_rate": 5000
        }
    )

    assert equipment_response.status_code == 201

    # Rent equipment
    rental_response = client.post(
        "/rentals",
        json={
            "customer_id": 200,
            "equipment_id": 200,
            "days": 3
        }
    )

    assert rental_response.status_code == 201

    rental = rental_response.json()

    assert rental["customer_id"] == 200
    assert rental["equipment_id"] == 200
    assert rental["days"] == 3
    assert rental["total_amount"] == 15000

    rental_id = rental["id"]

    # Equipment should now be unavailable
    equipment_response = client.get("/equipment")

    equipment = next(
        item for item in equipment_response.json()
        if item["id"] == 200
    )

    assert equipment["available"] is False

    # Trying to rent the same equipment again should fail
    second_rental = client.post(
        "/rentals",
        json={
            "customer_id": 200,
            "equipment_id": 200,
            "days": 2
        }
    )

    assert second_rental.status_code == 409

    # Return equipment
    return_response = client.post(
        f"/rentals/{rental_id}/return"
    )

    assert return_response.status_code == 200

    # Equipment should become available again
    equipment_response = client.get("/equipment")

    equipment = next(
        item for item in equipment_response.json()
        if item["id"] == 200
    )

    assert equipment["available"] is True

def test_register_user(client):

    response = client.post(
        "/auth/register",
        json={
            "username": "new_user",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "User registered successfully."
    assert data["username"] == "new_user"


def test_register_duplicate_user(client):

    client.post(
        "/auth/register",
        json={
            "username": "duplicate_user",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "duplicate_user",
            "password": "password123"
        }
    )

    assert response.status_code == 409


def test_login_user(client):

    client.post(
        "/auth/register",
        json={
            "username": "login_user",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "login_user",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):

    client.post(
        "/auth/register",
        json={
            "username": "wrong_password_user",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "wrong_password_user",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_protected_endpoint_without_token():

    from fastapi.testclient import TestClient

    unauthenticated_client = TestClient(app)

    response = unauthenticated_client.get("/equipment")

    assert response.status_code == 401