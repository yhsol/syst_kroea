from fastapi import FastAPI
from app.core.config import get_settings
from app.api.endpoints import trading, webhook

app = FastAPI(title="Trading System")

app.include_router(trading.router, prefix="/api/v1", tags=["trading"])
app.include_router(webhook.router, prefix="/api/v1/webhook", tags=["webhook"])

@app.get("/")
async def root():
    return {"message": "Trading System API"}

