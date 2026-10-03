import pytest
from fastapi import HTTPException
import services.rental_service as rental_service


def test_create_rental(monkeypatch):

    monkeypatch.setattr(
        rental_service,
        "get_customer_by_id",
        lambda customer_id: (2, "XYZ Infrastructure", "9988776655", "xyz@example.com")
    )

    monkeypatch.setattr(
        rental_service,
        "get_equipment_by_id",
        lambda equipment_id: (2, "Toyota Forklift", "Forklift", 3000, 1)
    )

    monkeypatch.setattr(
        rental_service,
        "create_rental_transaction",
        lambda customer_id, equipment_id, days, total_amount: 99
    )

    result = rental_service.create_rental(
        customer_id=2,
        equipment_id=2,
        days=2
    )

    assert result["id"] == 99
    assert result["customer_id"] == 2
    assert result["equipment_id"] == 2
    assert result["days"] == 2
    assert result["total_amount"] == 6000


def test_rental_days_must_be_positive():

    with pytest.raises(HTTPException) as error:
        rental_service.create_rental(
            customer_id=2,
            equipment_id=2,
            days=0
        )

    assert error.value.status_code == 400
    assert error.value.detail == "Rental days must be greater than 0."


def test_customer_not_found(monkeypatch):

    monkeypatch.setattr(
        rental_service,
        "get_customer_by_id",
        lambda customer_id: None
    )

    with pytest.raises(HTTPException) as error:
        rental_service.create_rental(
            customer_id=999,
            equipment_id=2,
            days=2
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Customer not found."


def test_equipment_already_rented(monkeypatch):

    monkeypatch.setattr(
        rental_service,
        "get_customer_by_id",
        lambda customer_id: (2, "XYZ Infrastructure", "9988776655", "xyz@example.com")
    )

    monkeypatch.setattr(
        rental_service,
        "get_equipment_by_id",
        lambda equipment_id: (2, "Toyota Forklift", "Forklift", 3000, 0)
    )

    with pytest.raises(HTTPException) as error:
        rental_service.create_rental(
            customer_id=2,
            equipment_id=2,
            days=2
        )

    assert error.value.status_code == 409
    assert error.value.detail == "Equipment is already rented."