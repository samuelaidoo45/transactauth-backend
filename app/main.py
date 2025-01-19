from fastapi import FastAPI
from app.routers import users
from app.database import engine, Base
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware



# Create tables on application start
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins for better security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom FastAPI API",
        version="1.0.0",
        description="Custom API with selective Bearer Token Authentication",
        routes=app.routes,
    )
    # Add Bearer Token Security Scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Apply Security Only to Specific Endpoints
    for path, methods in openapi_schema["paths"].items():
        for method, details in methods.items():
            if path == "/users/me":  # Apply BearerAuth to /users/me only
                details["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Override the default OpenAPI schema with the custom one
app.openapi = custom_openapi

# Include routers
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Authentication API!"}
