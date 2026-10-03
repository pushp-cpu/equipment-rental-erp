from pydantic import BaseModel


class EquipmentCreate(BaseModel):
    name: str
    equipment_type: str
    daily_rate: float


class EquipmentResponse(BaseModel):
    id: int
    name: str
    equipment_type: str
    daily_rate: float
    available: bool


class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: str


class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str


class RentalCreate(BaseModel):
    customer_id: int
    equipment_id: int
    days: int


class RentalResponse(BaseModel):
    id: int
    customer_id: int
    customer_name: str
    equipment_id: int
    equipment_name: str
    days: int
    total_amount: float
    returned: bool