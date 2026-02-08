from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Create a limiter instance
limiter = Limiter(key_func=get_remote_address)

def add_rate_limiter(app: FastAPI):
    """
    Adds rate limiting to the FastAPI application
    """
    app.state.limiter = limiter
    # Add exception handler for rate limit exceeded
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded_handler(request, exc):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"}
        )