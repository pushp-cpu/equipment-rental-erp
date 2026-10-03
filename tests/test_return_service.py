import pytest
from fastapi import HTTPException
import services.return_service as return_service


def test_rental_not_found(monkeypatch):

    monkeypatch.setattr(
        return_service,
        "get_rental_by_id",
        lambda rental_id: None
    )

    with pytest.raises(HTTPException) as error:
        return_service.return_equipment(999)

    assert error.value.status_code == 404
    assert error.value.detail == "Rental not found."


def test_rental_already_returned(monkeypatch):

    monkeypatch.setattr(
        return_service,
        "get_rental_by_id",
        lambda rental_id: (2, 2, 3, 5, 30000, 1)
    )

    with pytest.raises(HTTPException) as error:
        return_service.return_equipment(2)

    assert error.value.status_code == 409
    assert error.value.detail == "Rental has already been returned."


def test_successful_return(monkeypatch):

    monkeypatch.setattr(
        return_service,
        "get_rental_by_id",
        lambda rental_id: (2, 2, 3, 5, 30000, 0)
    )

    monkeypatch.setattr(
        return_service,
        "return_rental",
        lambda rental_id: 3
    )

    result = return_service.return_equipment(2)

    assert result["message"] == "Equipment returned successfully."
    assert result["rental_id"] == 2
    assert result["equipment_id"] == 3