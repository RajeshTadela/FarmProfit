from pydantic import BaseModel

class FarmerCreate(BaseModel):
    name: str
    age: int
    mobile: str
    village: str

from sqlalchemy import Column,Integer,String,Float,ForeignKey,Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Farmer(Base):

    __tablename__ = "farmers"

    farmer_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String(100))

    age = Column(Integer)

    mobile = Column(String(15))

    village = Column(String(100))

    username = Column(
        String(50),
        unique=True
    )

    password = Column(String(255))

class Field(Base):
    __tablename__ = "fields"

    field_id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.farmer_id"))
    field_name = Column(String(100))
    area_acres = Column(Integer)

from sqlalchemy import Date
from sqlalchemy import DECIMAL

class Driver(Base):

    __tablename__ = "drivers"

    driver_id = Column(Integer, primary_key=True, index=True)

    farmer_id = Column(Integer, ForeignKey("farmers.farmer_id"))

    driver_name = Column(String)

    mobile = Column(String)

    total_amount = Column(Float, default=0)

    total_paid = Column(Float, default=0)

    balance_amount = Column(Float, default=0)


class Plowing(Base):

    __tablename__ = "plowing"

    plowing_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    field_id = Column(
        Integer,
        ForeignKey("fields.field_id")
    )

    driver_id = Column(
        Integer,
        ForeignKey("drivers.driver_id")
    )

    plowing_date = Column(
        Date
    )

    hours_worked = Column(
        Float
    )

    rate_per_hour = Column(
        Float
    )

    plowing_round = Column(
        Integer
    )

    total_amount = Column(
        Float
    )
    
    today_plowings = Column(Integer)
class DriverPayment(Base):

    __tablename__ = "driver_payments"

    payment_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    driver_id = Column(
        Integer,
        ForeignKey("drivers.driver_id")
    )

    payment_date = Column(Date)

    amount_paid = Column(Float)