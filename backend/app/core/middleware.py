import time
from collections import defaultdict
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SecureHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, hsts_seconds: int = 63072000):
        super().__init__(app)
        self.hsts_seconds = hsts_seconds

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Strict-Transport-Security"] = f"max-age={self.hsts_seconds}; includeSubDomains"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 120, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        queue = self._requests[ip]
        # remove expired timestamps
        while queue and queue[0] + self.window_seconds < now:
            queue.pop(0)
        if len(queue) >= self.max_requests:
            return Response(
                status_code=429,
                content="Rate limit exceeded. Try again later.",
            )
        queue.append(now)
        return await call_next(request)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            # Keep internal details out of the response
            from fastapi.responses import JSONResponse
            from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"},
            )


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exclude_paths=None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or ["/login", "/api/v1/auth/login", "/health"]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path in self.exclude_paths or request.url.path.startswith("/static"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # Redirect to login for HTML pages
            if request.headers.get("accept", "").startswith("text/html"):
                return RedirectResponse(url="/login", status_code=302)
            return Response(status_code=401, content="Unauthorized")

        return await call_next(request)
