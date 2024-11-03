from fastapi import APIRouter, Depends, HTTPException
from app.services.trading_service import TradingService
from app.core.config import get_settings

router = APIRouter()

@router.get("/balance")
async def get_balance(
    trading_service: TradingService = Depends(TradingService)
):
    balance, holdings = trading_service.get_balance()
    return {
        "total_balance": balance,
        "holdings": holdings.to_dict(orient='records') if not holdings.empty else []
    }

@router.get("/current-price/{stock_code}")
async def get_current_price(
    stock_code: str,
    trading_service: TradingService = Depends(TradingService)
):
    result = trading_service.get_current_price(stock_code)
    if not result:
        raise HTTPException(status_code=404, detail="Stock not found")
    return result

@router.get("/hoga/{stock_code}")
async def get_hoga(
    stock_code: str,
    trading_service: TradingService = Depends(TradingService)
):
    result = trading_service.get_hoga_info(stock_code)
    if not result:
        raise HTTPException(status_code=404, detail="Hoga info not found")
    return result

@router.get("/fluctuation-rank")
async def get_fluctuation_rank(
    trading_service: TradingService = Depends(TradingService)
):
    result = trading_service.get_fluctuation_rank()
    if not result:
        raise HTTPException(status_code=404, detail="Fluctuation rank not found")
    return result

@router.post("/order/buy")
async def place_buy_order(
    stock_code: str,
    quantity: int,
    price: float,
    order_type: str = "01",
    trading_service: TradingService = Depends(TradingService)
):
    result = trading_service.place_buy_order(stock_code, quantity, price, order_type)
    if not result:
        raise HTTPException(status_code=400, detail="Order failed")
    return result

@router.post("/order/sell")
async def place_sell_order(
    stock_code: str,
    quantity: int,
    price: float,
    order_type: str = "01",
    trading_service: TradingService = Depends(TradingService)
):
    result = trading_service.place_sell_order(stock_code, quantity, price, order_type)
    if not result:
        raise HTTPException(status_code=400, detail="Order failed")
    return result

@router.get("/orders")
async def get_orders(
    trading_service: TradingService = Depends(TradingService)
):
    result = trading_service.get_orders()
    if result is None:
        raise HTTPException(status_code=404, detail="Orders not found")
    return result.to_dict(orient='records') if not result.empty else []

@router.post("/order/cancel")
async def cancel_order(
    order_no: str,
    quantity: int,
    price: str = "01",
    trading_service: TradingService = Depends(TradingService)
):
    result = trading_service.cancel_order(order_no, quantity, price)
    if not result:
        raise HTTPException(status_code=400, detail="Cancel failed")
    return result

# 해외주식 관련 엔드포인트 추가
@router.get("/overseas/current-price/{exchange_code}/{stock_code}")
async def get_current_price_overseas(
    exchange_code: str,
    stock_code: str,
    trading_service: TradingService = Depends(TradingService)
):
    result = trading_service.get_current_price_overseas(exchange_code, stock_code)
    if not result:
        raise HTTPException(status_code=404, detail="Stock not found")
    return result

@router.get("/overseas/balance")
async def get_balance_overseas(
    trading_service: TradingService = Depends(TradingService)
):
    balance, holdings = trading_service.get_balance_overseas()
    return {
        "total_profit_loss": balance,
        "holdings": holdings.to_dict(orient='records') if not holdings.empty else []
    }

@router.post("/overseas/order/buy")
async def place_buy_order_overseas(
    exchange_code: str,
    stock_code: str,
    price: float,
    quantity: int,
    order_type: str = "00",
    trading_service: TradingService = Depends(TradingService)
):
    result = trading_service.place_buy_order_overseas(exchange_code, stock_code, price, quantity, order_type)
    if not result:
        raise HTTPException(status_code=400, detail="Order failed")
    return result

@router.post("/overseas/order/sell")
async def place_sell_order_overseas(
    exchange_code: str,
    stock_code: str,
    price: float,
    quantity: int,
    order_type: str = "00",
    trading_service: TradingService = Depends(TradingService)
):
    result = trading_service.place_sell_order_overseas(exchange_code, stock_code, price, quantity, order_type)
    if not result:
        raise HTTPException(status_code=400, detail="Order failed")
    return result 