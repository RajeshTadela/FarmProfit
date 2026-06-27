from fastapi import FastAPI
from database import SessionLocal
from models import Base
from database import engine
from models import Farmer
from schemas import (
    FarmerCreate,
    FieldCreate,
    PlowingCreate,
    FarmerRegister,
    FarmerLogin
)
from models import DriverPayment
from schemas import DriverPaymentCreate

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.post("/farmers")
def create_farmer(farmer: FarmerCreate):

    db = SessionLocal()

    new_farmer = Farmer(
        name=farmer.name,
        age=farmer.age,
        mobile=farmer.mobile,
        village=farmer.village
    )

    db.add(new_farmer)

    db.commit()

    db.refresh(new_farmer)

    db.close()

    return {
        "message": "Farmer created successfully"
    }

@app.get("/farmers")
def get_farmers():

    db = SessionLocal()
    farmers = db.query(Farmer).all()
    db.close()

    return farmers

from models import Farmer, Field

@app.post("/fields")
def create_field(field: FieldCreate):

    db = SessionLocal()

    new_field = Field(
        farmer_id=field.farmer_id,
        field_name=field.field_name,
        area_acres=field.area_acres
    )

    db.add(new_field)
    db.commit()
    db.refresh(new_field)

    db.close()

    return {
        "message": "Field created successfully"
    }

@app.get("/fields")
def get_fields():

    db = SessionLocal()
    fields = db.query(Field).all()
    db.close()

    return fields

from models import Farmer, Field

from sqlalchemy import func

@app.get("/field-summary/{field_id}")
def field_summary(field_id: int):

    db = SessionLocal()

    field = (
        db.query(Field)
        .filter(Field.field_id == field_id)
        .first()
    )

    total_plowings = (
        db.query(func.count(Plowing.plowing_id))
        .filter(Plowing.field_id == field_id)
        .scalar()
    )

    total_hours = (
        db.query(func.sum(Plowing.hours_worked))
        .filter(Plowing.field_id == field_id)
        .scalar()
    )

    total_expense = (
        db.query(func.sum(Plowing.total_cost))
        .filter(Plowing.field_id == field_id)
        .scalar()
    )

    db.close()

    return {
        "field_name": field.field_name,
        "total_plowings": total_plowings,
        "total_hours": total_hours,
        "total_expense": total_expense
    }

@app.get("/farmer-dashboard/{farmer_id}")
def farmer_dashboard(farmer_id: int):

    db = SessionLocal()

    farmer = (
        db.query(Farmer)
        .filter(Farmer.farmer_id == farmer_id)
        .first()
    )

    total_fields = (
        db.query(func.count(Field.field_id))
        .filter(Field.farmer_id == farmer_id)
        .scalar()
    )

    field_ids = (
        db.query(Field.field_id)
        .filter(Field.farmer_id == farmer_id)
        .all()
    )

    field_ids = [f[0] for f in field_ids]

    total_plowing_records = (
        db.query(func.count(Plowing.plowing_id))
        .filter(Plowing.field_id.in_(field_ids))
        .scalar()
    )

    total_plowing_expense = (
        db.query(func.sum(Plowing.total_cost))
        .filter(Plowing.field_id.in_(field_ids))
        .scalar()
    )

    db.close()

    return {
        "farmer_name": farmer.name,
        "total_fields": total_fields,
        "total_plowing_records": total_plowing_records,
        "total_plowing_expense": total_plowing_expense or 0
    }

@app.post("/register")
def register_farmer(farmer: FarmerRegister):

    db = SessionLocal()

    # Username already exists?
    existing_user = (
        db.query(Farmer)
        .filter(
            Farmer.username == farmer.username
        )
        .first()
    )

    if existing_user:

        db.close()

        return {
            "success": False,
            "message":
            "Username already exists"
        }

    # Username length validation
    if len(farmer.username) < 6:

        db.close()

        return {
            "success": False,
            "message":
            "Username must be at least 6 characters"
        }

    new_farmer = Farmer(
    username=farmer.username,
    password=farmer.password
    )

    db.add(new_farmer)

    db.commit()

    db.refresh(new_farmer)

    db.close()

    return {
        "success": True,
        "message":
        "Account created successfully"
    }


@app.post("/login")
def login_farmer(user: FarmerLogin):

    db = SessionLocal()

    farmer = (
        db.query(Farmer)
        .filter(
            Farmer.username == user.username
        )
        .first()
    )

    if not farmer:

        db.close()

        return {
            "success": False,
            "message":
            "Username not found"
        }

    if farmer.password != user.password:

        db.close()

        return {
            "success": False,
            "message":
            "Incorrect password"
        }

    db.close()

    return {
        "success": True,
        "message":
        "Login Successful",
        "farmer_id":
        farmer.farmer_id
    }

from schemas import ProfileCreate
@app.put("/profile")
def save_profile(profile: ProfileCreate):

    db = SessionLocal()

    farmer = (
        db.query(Farmer)
        .filter(
            Farmer.farmer_id == profile.farmer_id
        )
        .first()
    )

    farmer.name = profile.name
    farmer.age = profile.age
    farmer.mobile = profile.mobile
    farmer.village = profile.village

    db.commit()

    db.close()

    return {
        "success": True,
        "message": "Profile Saved"
    }

@app.get("/farmer/{farmer_id}")
def get_farmer(farmer_id: int):

    db = SessionLocal()

    farmer = (
        db.query(Farmer)
        .filter(
            Farmer.farmer_id == farmer_id
        )
        .first()
    )

    db.close()

    return {
        "name": farmer.name,
        "age": farmer.age,
        "mobile": farmer.mobile,
        "village": farmer.village
    }

@app.get("/total-land/{farmer_id}")
def total_land(farmer_id: int):

    db = SessionLocal()

    total_land = (
        db.query(func.sum(Field.area_acres))
        .filter(Field.farmer_id == farmer_id)
        .scalar()
    )

    db.close()

    return {
        "total_land": total_land or 0
    }

@app.get("/farmer-fields/{farmer_id}")
def get_farmer_fields(farmer_id: int):

    db = SessionLocal()

    fields = (
        db.query(Field)
        .filter(
            Field.farmer_id == farmer_id
        )
        .all()
    )

    result = []

    for field in fields:

        result.append(
            {
                "field_id": field.field_id,
                "field_name": field.field_name,
                "area_acres": field.area_acres
            }
        )

    db.close()

    return result

@app.put("/field/{field_id}")
def update_field(
    field_id: int,
    field: FieldCreate
):

    db = SessionLocal()

    existing_field = (
        db.query(Field)
        .filter(
            Field.field_id == field_id
        )
        .first()
    )

    if not existing_field:

        db.close()

        return {
            "success": False,
            "message": "Field not found"
        }

    existing_field.field_name = field.field_name
    existing_field.area_acres = field.area_acres

    db.commit()

    db.close()

    return {
        "success": True,
        "message": "Field Updated"
    }

@app.delete("/field/{field_id}")
def delete_field(field_id: int):

    db = SessionLocal()

    field = (
        db.query(Field)
        .filter(
            Field.field_id == field_id
        )
        .first()
    )

    if not field:

        db.close()

        return {
            "success": False,
            "message": "Field not found"
        }

    db.delete(field)

    db.commit()

    db.close()

    return {
        "success": True,
        "message": "Field Deleted"
    }

from models import Plowing,Driver
from schemas import PlowingCreate,DriverCreate

@app.post("/driver")
def create_driver(driver: DriverCreate):

    db = SessionLocal()

    new_driver = Driver(
        farmer_id=driver.farmer_id,
        driver_name=driver.driver_name
    )

    db.add(new_driver)

    db.commit()

    db.refresh(new_driver)

    db.close()

    return {
        "success": True,
        "message": "Driver Added Successfully"
    }

@app.get("/drivers/{farmer_id}")
def get_drivers(farmer_id: int):

    db = SessionLocal()

    drivers = (
        db.query(Driver)
        .filter(
            Driver.farmer_id == farmer_id
        )
        .all()
    )

    result = []

    for driver in drivers:

        total_work = (
            driver.total_amount
            if driver.total_amount
            else 0
        )

        total_paid = (
            driver.total_paid
            if driver.total_paid
            else 0
        )

        balance = total_work - total_paid

        result.append(
            {
                "driver_id": driver.driver_id,
                "driver_name": driver.driver_name,
                "total_amount": total_work,
                "total_paid": total_paid,
                "balance_amount": balance
            }
        )

    db.close()

    return result

#PLOWING API'S

@app.post("/plowing")
def create_plowing(plowing: PlowingCreate):

    db = SessionLocal()

    total_amount = (
        plowing.hours_worked *
        plowing.rate_per_hour
    )

    new_plowing = Plowing(
    field_id=plowing.field_id,
    driver_id=plowing.driver_id,
    plowing_date=plowing.plowing_date,
    hours_worked=plowing.hours_worked,
    rate_per_hour=plowing.rate_per_hour,
    plowing_round=plowing.plowing_round,
    today_plowings=plowing.today_plowings,
    total_amount=total_amount
)
    db.add(new_plowing)

    # -------------------------
    # UPDATE DRIVER TOTALS
    # -------------------------

    driver = db.query(Driver).filter(
        Driver.driver_id == plowing.driver_id
    ).first()

    driver.total_amount += total_amount
    driver.balance_amount += total_amount

    db.commit()

    db.refresh(new_plowing)

    db.close()

    return {
        "success": True
    }

@app.get("/plowing-records/{farmer_id}")
def plowing_records(farmer_id: int):

    db = SessionLocal()

    records = (
        db.query(Plowing, Field, Driver)
        .join(Field, Plowing.field_id == Field.field_id)
        .join(Driver, Plowing.driver_id == Driver.driver_id)
        .filter(Field.farmer_id == farmer_id)
        .order_by(Plowing.plowing_date.desc())
        .all()
    )

    result = []

    for plowing, field, driver in records:

        result.append({
            "field_name": field.field_name,
            "area": field.area_acres,
            "date": str(plowing.plowing_date),
            "hours": plowing.hours_worked,
            "driver": driver.driver_name,
            "today_plowings": plowing.today_plowings,
            "amount": plowing.total_amount
        })

    db.close()

    return result




@app.post("/driver-payment")
def pay_driver(payment: DriverPaymentCreate):

    db = SessionLocal()

    new_payment = DriverPayment(
        driver_id=payment.driver_id,
        payment_date=payment.payment_date,
        amount_paid=payment.amount_paid
    )

    db.add(new_payment)

    driver = db.query(Driver).filter(
        Driver.driver_id == payment.driver_id
    ).first()

    driver.total_paid += payment.amount_paid
    driver.balance_amount -= payment.amount_paid

    db.commit()

    db.close()

    return {
        "success": True
    }

@app.get("/driver-balance/{driver_id}")
def driver_balance(driver_id:int):

    db = SessionLocal()

    total_work = (

        db.query(

            func.sum(

                Plowing.total_amount

            )

        )

        .filter(

            Plowing.driver_id==driver_id

        )

        .scalar()

    ) or 0

    total_paid = (

        db.query(

            func.sum(

                DriverPayment.amount_paid

            )

        )

        .filter(

            DriverPayment.driver_id==driver_id

        )

        .scalar()

    ) or 0

    db.close()

    return{

        "total_work":total_work,

        "total_paid":total_paid,

        "balance":total_work-total_paid

    }

@app.get("/driver-payment-history/{driver_id}")
def payment_history(driver_id:int):

    db=SessionLocal()

    history=(

        db.query(

            DriverPayment

        )

        .filter(

            DriverPayment.driver_id==driver_id

        )

        .all()

    )

    db.close()

    return history

@app.get("/driver-payment-records/{farmer_id}")
def driver_payment_records(farmer_id: int):

    db = SessionLocal()

    drivers = (
        db.query(Driver)
        .filter(Driver.farmer_id == farmer_id)
        .all()
    )

    result = []

    for driver in drivers:

        # Total Paid
        total_paid = (
            db.query(func.sum(DriverPayment.amount_paid))
            .filter(DriverPayment.driver_id == driver.driver_id)
            .scalar()
        ) or 0

        # Last Payment Date
        last_payment = (
            db.query(func.max(DriverPayment.payment_date))
            .filter(DriverPayment.driver_id == driver.driver_id)
            .scalar()
        )

        result.append({

            "Driver": driver.driver_name,

            "Last Payment Date": last_payment if last_payment else "Never Paid",

            "Total Paid": total_paid,

            "Balance": driver.balance_amount

        })

    db.close()

    return result


@app.get("/plowing/{field_id}")
def get_plowing(field_id: int):

    db = SessionLocal()

    records = (
        db.query(Plowing)
        .filter(
            Plowing.field_id == field_id
        )
        .all()
    )

    result = []

    for record in records:

        result.append({
            "plowing_id": record.plowing_id,
            "driver_id": record.driver_id,
            "today_plowings": record.today_plowings,
            "hours_worked": record.hours_worked,
            "total_amount": record.total_amount
        })

    db.close()

    return result

@app.get("/driver-summary/{driver_id}")
def driver_summary(driver_id: int):

    db = SessionLocal()

    total_jobs = (
        db.query(func.count(Plowing.plowing_id))
        .filter(
            Plowing.driver_id == driver_id
        )
        .scalar()
    )

    total_hours = (
        db.query(func.sum(Plowing.hours_worked))
        .filter(
            Plowing.driver_id == driver_id
        )
        .scalar()
    )

    total_earnings = (
        db.query(func.sum(Plowing.total_amount))
        .filter(
            Plowing.driver_id == driver_id
        )
        .scalar()
    )

    db.close()

    return {
        "total_jobs": total_jobs or 0,
        "total_hours": total_hours or 0,
        "total_earnings": total_earnings or 0,
    }

@app.put("/driver/{driver_id}")
def update_driver(driver_id: int, driver: DriverCreate):

    db = SessionLocal()

    existing_driver = (
        db.query(Driver)
        .filter(
            Driver.driver_id == driver_id
        )
        .first()
    )

    if not existing_driver:

        db.close()

        return {
            "success": False,
            "message": "Driver not found"
        }

    existing_driver.driver_name = driver.driver_name
    db.commit()

    db.close()

    return {
        "success": True,
        "message": "Driver Updated"
    }


@app.delete("/driver/{driver_id}")
def delete_driver(driver_id: int):

    db = SessionLocal()

    driver = (
        db.query(Driver)
        .filter(
            Driver.driver_id == driver_id
        )
        .first()
    )

    if not driver:

        db.close()

        return {
            "success": False,
            "message": "Driver not found"
        }

    db.delete(driver)

    db.commit()

    db.close()

    return {
        "success": True,
        "message": "Driver Deleted"
    }

