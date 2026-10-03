from fastapi import HTTPException

from database import (
    get_rental_by_id,
    return_rental
)


def return_equipment(rental_id):

    rental = get_rental_by_id(rental_id)

    if rental is None:
        raise HTTPException(
            status_code=404,
            detail="Rental not found."
        )

    if rental[5] == 1:
        raise HTTPException(
            status_code=409,
            detail="Rental has already been returned."
        )

    equipment_id = return_rental(rental_id)

    return {
        "message": "Equipment returned successfully.",
        "rental_id": rental_id,
        "equipment_id": equipment_id
    }