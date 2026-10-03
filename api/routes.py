from fastapi import APIRouter, HTTPException, Depends
from services.rental_service import create_rental
from services.return_service import return_equipment
import sqlite3
from auth_dependencies import get_current_user
from fastapi import Depends
from equipment import Equipment
from customer import Customer
from auth import (
    hash_password,
    verify_password,
    create_access_token
)

from models.auth_schemas import (
    UserCreate,
    UserLogin,
    TokenResponse
)

from database import (
    # keep your existing imports
    create_user,
    get_user_by_username
)

from models.schemas import (
    EquipmentCreate,
    EquipmentResponse,
    CustomerCreate,
    CustomerResponse,
    RentalCreate,
    RentalResponse
)

from database import (
    create_user,
    get_user_by_username,
    add_equipment_to_db,
    get_all_equipment,
    get_equipment_by_id,
    update_equipment_availability,
    add_customer_to_db,
    get_all_customers,
    get_customer_by_id,
    get_all_rentals_detailed,
    create_rental_transaction,
    get_rental_by_id,
    return_rental
)

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "equipment-rental-erp"
    }


@router.get("/customers", response_model=list[CustomerResponse])
def get_customers(current_user: str = Depends(get_current_user)):
    customers = get_all_customers()

    return [
        {
            "id": item[0],
            "name": item[1],
            "phone": item[2],
            "email": item[3]
        }
        for item in customers
    ]


@router.post("/customers", response_model=CustomerResponse, status_code=201)
def create_customer(
    customer_data: CustomerCreate,
    current_user: str = Depends(get_current_user)
):
    customer = Customer(
        None,
        customer_data.name,
        customer_data.phone,
        customer_data.email
    )

    customer_id = add_customer_to_db(customer)

    return {
        "id": customer_id,
        "name": customer.name,
        "phone": customer.phone,
        "email": customer.email
    }




@router.get("/equipment", response_model=list[EquipmentResponse])
def get_equipment(current_user: str = Depends(get_current_user)):
    equipment = get_all_equipment()

    return [
        {
            "id": item[0],
            "name": item[1],
            "equipment_type": item[2],
            "daily_rate": item[3],
            "available": bool(item[4])
        }
        for item in equipment
    ]


@router.post("/equipment", response_model=EquipmentResponse, status_code=201)
def create_equipment(
    equipment_data: EquipmentCreate,
    current_user: str = Depends(get_current_user)
):
    equipment = Equipment(
        None,
        equipment_data.name,
        equipment_data.equipment_type,
        equipment_data.daily_rate
    )

    equipment_id = add_equipment_to_db(equipment)

    return {
        "id": equipment_id,
        "name": equipment.name,
        "equipment_type": equipment.equipment_type,
        "daily_rate": equipment.daily_rate,
        "available": equipment.available
    }


@router.post("/rentals", response_model=RentalResponse, status_code=201)
def create_rental_endpoint(
    rental_data: RentalCreate,
    current_user: str = Depends(get_current_user)
):
    return create_rental(
        rental_data.customer_id,
        rental_data.equipment_id,
        rental_data.days
    )


@router.get("/rentals", response_model=list[RentalResponse])
def get_rentals(current_user: str = Depends(get_current_user)):
    rentals = get_all_rentals_detailed()

    return [
        {
            "id": item[0],
            "customer_id": item[1],
            "customer_name": item[2],
            "equipment_id": item[3],
            "equipment_name": item[4],
            "days": item[5],
            "total_amount": item[6],
            "returned": bool(item[7])
        }
        for item in rentals
    ]

@router.post("/rentals/{rental_id}/return")
def return_equipment_endpoint(
    rental_id: int,
    current_user: str = Depends(get_current_user)
):
    return return_equipment(rental_id)

@router.post(
    "/auth/register",
    status_code=201
)
def register_user(user_data: UserCreate):

    existing_user = get_user_by_username(user_data.username)

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="Username already exists."
        )

    password_hash = hash_password(user_data.password)

    create_user(
        user_data.username,
        password_hash
    )

    return {
        "message": "User registered successfully.",
        "username": user_data.username
    }


@router.post(
    "/auth/login",
    response_model=TokenResponse
)
def login_user(user_data: UserLogin):

    user = get_user_by_username(user_data.username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    if not verify_password(
        user_data.password,
        user[2]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    token = create_access_token(
        user_data.username
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }