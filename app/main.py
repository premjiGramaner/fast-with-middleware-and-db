from fastapi import FastAPI, Depends
from pydantic import BaseModel
from app.core.security import verify_token
from app.db.database import Base, engine
from app.api.routes import employee, unauth

from app.core.middleware import AuthMiddleware

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBearer

app = FastAPI()
security = HTTPBearer()

# Default route to validate the application is running

# Create DB
Base.metadata.create_all(bind=engine)

# Apply middleware
app.add_middleware(AuthMiddleware)

# Disable Swagger (Production)
# app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


class PostArgs(BaseModel):
    value: str


@app.post("/ping")
def ping(args: PostArgs):
    return {"message": f"Return value: {args.value}"}


@app.get("/swagger", include_in_schema=False)
def custom_swagger():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Custom Swagger UI"
    )


@app.get("/protected", tags=["Auth"])
def protected(token: str = Depends(verify_token)):
    return {"message": "Access granted"}


app.include_router(employee.router, prefix="/api/v1")
app.include_router(unauth.router, prefix="/api/v2")
