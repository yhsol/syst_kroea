from fastapi import FastAPI
from app.core.config import get_settings
from app.api.endpoints import trading

app = FastAPI(title="Trading System")

app.include_router(trading.router, prefix="/api/v1", tags=["trading"])

@app.get("/")
async def root():
    return {"message": "Trading System API"}
