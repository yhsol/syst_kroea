from fastapi import FastAPI
from app.core.config import get_settings
from app.api.v1.trading import router as trading_router
from app.api.v1.webhook import router as webhook_router
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(message)s'
)

app = FastAPI(title="Trading System")

app.include_router(trading_router, prefix="/api/v1/trading", tags=["trading"])
app.include_router(webhook_router, prefix="/api/v1/webhook", tags=["webhook"])

@app.get("/")
async def root():
    return {"message": "Trading System API"}

