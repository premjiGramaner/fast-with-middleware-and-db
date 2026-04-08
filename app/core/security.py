from jose import jwt, JWTError
from fastapi import HTTPException

from app.core.constants import ALGORITHM, SECRET_KEY


# 🔍 Verify JWT Token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract required fields
        username = payload.get("sub")
        role = payload.get("role")

        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid token payload")

        return {
            "sub": username,
            "role": role
        }

    except JWTError as e:
        raise HTTPException(
            status_code=401, detail=f"Invalid or expired token: {e}") from e
