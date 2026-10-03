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
            "name": "Test Construction",
            "phone": "9999999999",
            "email": "test@example.com"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["name"] == "Test Construction"
    assert data["phone"] == "9999999999"
    assert data["email"] == "test@example.com"


def test_create_customer_multiple_customers(client):

    response_1 = client.post(
        "/customers",
        json={
            "name": "First Company",
            "phone": "9999999999",
            "email": "first@example.com"
        }
    )

    response_2 = client.post(
        "/customers",
        json={
            "name": "Second Company",
            "phone": "8888888888",
            "email": "second@example.com"
        }
    )

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    id_1 = response_1.json()["id"]
    id_2 = response_2.json()["id"]

    assert id_1 > 0
    assert id_2 > 0
    assert id_1 != id_2


def test_create_rental_and_return(client):

    # Create customer
    customer_response = client.post(
        "/customers",
        json={
            "name": "Rental Test Company",
            "phone": "8888888888",
            "email": "rental@test.com"
        }
    )

    assert customer_response.status_code == 201

    customer_id = customer_response.json()["id"]

    # Create equipment
    equipment_response = client.post(
        "/equipment",
        json={
            "name": "Test Excavator",
            "equipment_type": "Excavator",
            "daily_rate": 5000
        }
    )

    assert equipment_response.status_code == 201

    equipment_id = equipment_response.json()["id"]

    # Create rental
    rental_response = client.post(
        "/rentals",
        json={
            "customer_id": customer_id,
            "equipment_id": equipment_id,
            "days": 3
        }
    )

    assert rental_response.status_code == 201

    rental_data = rental_response.json()

    assert rental_data["customer_id"] == customer_id
    assert rental_data["equipment_id"] == equipment_id
    assert rental_data["days"] == 3
    assert rental_data["total_amount"] == 15000
    assert rental_data["returned"] is False

    rental_id = rental_data["id"]

    # Equipment should now be unavailable
    equipment_response = client.get("/equipment")

    equipment = next(
        item for item in equipment_response.json()
        if item["id"] == equipment_id
    )

    assert equipment["available"] is False

    # Trying to rent the same equipment again should fail
    second_rental = client.post(
        "/rentals",
        json={
            "customer_id": customer_id,
            "equipment_id": equipment_id,
            "days": 2
        }
    )

    assert second_rental.status_code == 409

    # Return equipment
    return_response = client.post(
        f"/rentals/{rental_id}/return"
    )

    assert return_response.status_code == 200

    return_data = return_response.json()

    assert return_data["rental_id"] == rental_id
    assert return_data["equipment_id"] == equipment_id

    # Equipment should become available again
    equipment_response = client.get("/equipment")

    equipment = next(
        item for item in equipment_response.json()
        if item["id"] == equipment_id
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

    unauthenticated_client = TestClient(app)

    response = unauthenticated_client.get("/equipment")

    assert response.status_code == 401