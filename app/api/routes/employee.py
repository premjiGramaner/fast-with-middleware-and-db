from fastapi import APIRouter, Depends, Form
from app.schemas.item import EmployeesResponse
from app.db.database import SessionLocal
from app.db import models

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/employee/")
def create_employee(
    name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db=Depends(get_db)
):

    try:
        employeeInfo = models.User(
            name=name,
            username=username,
            email=email,
            password=password,
            role=role
        )

        db.add(employeeInfo)
        db.commit()
        db.refresh(employeeInfo)

        return {
            "message": "Employee created successfully",
            "payload": {
                "id": employeeInfo.id,  # now available
                "name": employeeInfo.name,
                "username": employeeInfo.username,
                "email": employeeInfo.email,
                "role": employeeInfo.role
            }
        }

    except IntegrityError as e:
        db.rollback()  # Rollback the transaction on error

        raise HTTPException(
            status_code=400,
            detail={
                "message": "Employee creation failed",
                "query": str(e.statement),
                "error": str(e.orig),
            },
        ) from e


@router.get("/employees", response_model=EmployeesResponse)
def get_employees(db=Depends(get_db)):
    employees = db.query(models.User).all()
    return {
        "message": "Employees retrieved successfully",
        "payload": [
            {
                "id": employee.id,
                "name": employee.name,
                "username": employee.username,
                "email": employee.email,
                "password": employee.password,
                "role": employee.role
            }
            for employee in employees
        ]
    }


@router.delete("/employee/{id}")
def delete_user(id: int, db=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail={"message": f"User is not found for this id: {id}"})

    db.delete(user)
    db.commit()

    return {"message": f"User with id: {id} is deleted successfully"}


@router.patch('/employee/{id}')
def update_user(
        id: int,
        name: str = Form(None),
        username: str = Form(None),
        email: str = Form(None),
        role: str = Form(None),
        password: str = Form(None),
        db=Depends(get_db)
):

    user_name = username
    user_email = email
    user_role = role
    _name = name

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "message": f"User is not found for this id: {id}"
            }
        )

    if _name is not None:
        user.name = _name

    if user_name is not None:
        userExist = db.query(models.User).filter(
            models.User.username == user_name).first()

        if userExist and (userExist.id != id):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": f"Username '{user_name}' is already taken by another user."}
            )

        user.username = user_name

    if user_email is not None:
        userExist = db.query(models.User).filter(
            models.User.email == user_email).first()

        if userExist and (userExist.id != id):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": f"email '{user_email}' is already taken by another user."}
            )

        user.email = user_email

    if user_role is not None:
        user.role = user_role

    if password is not None:
        user.password = password

    db.commit()
    db.refresh(user)

    return {
        "message": f"User with id: {id} is updated successfully",
        "payload": {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }
