from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from app.api.v1.trading import router as trading_router
from app.api.v1.webhook import router as webhook_router
from app.core.scheduler import setup_scheduler
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(message)s'
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_scheduler()
    yield
    # Shutdown (if needed)

app = FastAPI(
    title="Trading System",
    lifespan=lifespan
)

app.include_router(trading_router, prefix="/api/v1/trading", tags=["trading"])
app.include_router(webhook_router, prefix="/api/v1/webhook", tags=["webhook"])

@app.get("/")
async def root():
    return {"message": "Trading System API"}

