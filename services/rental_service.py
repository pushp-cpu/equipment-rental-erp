from fastapi import HTTPException

from database import (
    get_customer_by_id,
    get_equipment_by_id,
    create_rental_transaction
)


def create_rental(customer_id, equipment_id, days):

    if days <= 0:
        raise HTTPException(
            status_code=400,
            detail="Rental days must be greater than 0."
        )

    customer = get_customer_by_id(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    equipment = get_equipment_by_id(equipment_id)

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found."
        )

    if equipment[4] == 0:
        raise HTTPException(
            status_code=409,
            detail="Equipment is already rented."
        )

    total_amount = equipment[3] * days

    rental_id = create_rental_transaction(
        customer_id,
        equipment_id,
        days,
        total_amount
    )

    return {
        "id": rental_id,
        "customer_id": customer_id,
        "customer_name": customer[1],
        "equipment_id": equipment_id,
        "equipment_name": equipment[1],
        "days": days,
        "total_amount": total_amount,
        "returned": False
    }