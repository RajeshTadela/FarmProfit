from pydantic import BaseModel

class FarmerCreate(BaseModel):
    name: str
    age: int
    mobile: str
    village: str

class FieldCreate(BaseModel):
    farmer_id: int
    field_name: str
    area_acres: float

class FarmerRegister(BaseModel):
    username: str
    password: str

class FarmerLogin(BaseModel):
    username: str
    password: str

class ProfileCreate(BaseModel):

    farmer_id: int
    name: str
    age: int
    mobile: str
    village: str


class DriverCreate(BaseModel):

    farmer_id: int

    driver_name: str

    mobile: str


from datetime import date

class PlowingCreate(BaseModel):

    field_id: int

    driver_id: int

    plowing_date: date

    hours_worked: float

    rate_per_hour: float

    plowing_round: int
    today_plowings: int

class DriverPaymentCreate(BaseModel):

    driver_id: int

    payment_date: date

    amount_paid: float
