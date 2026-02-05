from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.routers import todos
from api.routers.auth import auth
from init_db import create_db_and_tables
from middleware.security_middleware import SecurityHeadersMiddleware
from utils.rate_limiting.rate_limiter import limiter, add_rate_limiter

app = FastAPI(
    title="Todo API",
    description="A full-featured todo application API",
    version="1.0.0"
)

# Add rate limiter
add_rate_limiter(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Create database and tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include routers
app.include_router(todos.router, prefix="/api", tags=["todos"])
app.include_router(auth.router, prefix="/api", tags=["auth"])

@app.get("/")
@limiter.limit("5/minute")
def read_root(request: Request):
    return {"message": "Welcome to the Todo API"}