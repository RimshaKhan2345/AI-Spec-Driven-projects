from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.requests import Request
from fastapi import HTTPException, status
from time import time


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple rate limiting middleware to prevent abuse
    """
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 3600):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        current_time = time()

        # Check rate limit
        if client_ip in self.requests:
            count, timestamp = self.requests[client_ip]
            if (current_time - timestamp) < self.window_seconds:
                if count >= self.max_requests:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded"
                    )
                else:
                    self.requests[client_ip] = (count + 1, timestamp)
            else:
                # Reset counter after window period
                self.requests[client_ip] = (1, current_time)
        else:
            self.requests[client_ip] = (1, current_time)

        response = await call_next(request)
        return response