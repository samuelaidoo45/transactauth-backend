from fastapi import FastAPI
from app.routers import example

app = FastAPI()

# Include routers
app.include_router(example.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
