from fastapi import Depends, APIRouter
from pydantic import BaseModel
from app.api.routes.employee import get_db
from app.db import models
from app.core.utils import create_access_token

router = APIRouter()


class AccessTokenRequest(BaseModel):
    username: str
    password: str


@router.post("/token", tags=["Auth"])
def generate_access_token(data: AccessTokenRequest, db=Depends(get_db)):
    userInfo = db.query(models.User).filter(
        models.User.username == data.username, models.User.password == data.password).first()

    # return {"message": "Logged in successfully"}

    if not userInfo:
        return {"message": "Invalid username or password"}

    token = create_access_token(userInfo)

    return {"message": "Logged in successfully", "access_token": token}
