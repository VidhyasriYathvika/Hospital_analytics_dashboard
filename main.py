from fastapi import FastAPI
from app.routers import analytics

app = FastAPI(title="Hospital Dashboard API")

app.include_router(analytics.router)

@app.get("/")
def home():
    return {"message": "Hospital Dashboard API running successfully"}
