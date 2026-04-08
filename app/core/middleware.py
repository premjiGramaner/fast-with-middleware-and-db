from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from app.core.security import verify_token


PUBLIC_PATHS = ["/api/v2/token", "/docs", "/openapi.json", '/ping', '/swagger']


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"**** Request URL: {request.url.path}")
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        token = request.headers.get("Authorization")

        if not token:
            return Response("You are Unauthorized", status_code=401)

        try:
            payload = verify_token(token.replace("Bearer ", ""))

        except Exception as e:
            return Response(f"Invalid Token Exception {str(e)}", status_code=401)

        request.state.user = payload["sub"]
        request.state.role = payload["role"]

        return await call_next(request)
