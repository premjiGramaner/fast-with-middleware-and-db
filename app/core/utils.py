from datetime import datetime, timedelta, timezone
from jose import jwt
from pydantic import BaseModel
from app.core.constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from copy import deepcopy


class AccessTokenRequest(BaseModel):
    username: str
    role: str
    email: str
    name: str


def create_access_token(userInfo: AccessTokenRequest):
    data = deepcopy(userInfo)

    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return jwt.encode({
        "exp": expire,
        "role": data.role,
        "email": data.email,
        "name": data.name,
        "sub": data.username
    },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
