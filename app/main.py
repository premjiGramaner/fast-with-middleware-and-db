from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Default route to validate the application is running


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


class PostArgs(BaseModel):
    value: str


@app.post("/ping")
def ping(args: PostArgs):
    return {"message": f"Return value: {args.value}"}
