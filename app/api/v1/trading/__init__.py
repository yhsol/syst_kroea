from app.core.constants import OrderType
from fastapi import APIRouter, Depends, HTTPException
from app.services.trading_service import TradingService
from app.core.config import get_settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

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

@router.get("/overseas/hoga/{exchange_code}/{stock_code}")
async def get_overseas_hoga(
    exchange_code: str,
    stock_code: str,
    trading_service: TradingService = Depends(TradingService)
):
    """해외주식 호가 정보 조회"""
    result = trading_service.get_hoga_info_overseas(exchange_code, stock_code)
    if not result:
        raise HTTPException(status_code=404, detail="Failed to get hoga information")
    return result

@router.get("/overseas/buyable-amount/{exchange_code}/{stock_code}")
async def get_overseas_buyable_amount(
    exchange_code: str,
    stock_code: str,
    price: float,
    trading_service: TradingService = Depends(TradingService)
):
    """해외주식 매수가능금액 조회"""
    result = trading_service.get_buyable_amount_overseas(exchange_code, stock_code, price)
    if not result:
        raise HTTPException(status_code=404, detail="Failed to get buyable amount")
    return result

@router.get("/overseas/max-buy-quantity/{exchange_code}/{stock_code}")
async def get_overseas_max_buy_quantity(
    exchange_code: str,
    stock_code: str,
    trading_service: TradingService = Depends(TradingService)
):
    """해외주식 최대 매수 가능 수량 조회"""
    result = trading_service.calculate_overseas_max_buy_quantity(exchange_code, stock_code)
    if not result:
        raise HTTPException(status_code=404, detail="Failed to calculate max buy quantity")
    return {
        "max_quantity": result,
        "exchange_code": exchange_code,
        "stock_code": stock_code
    }

# 시장가 매수 기능 추가
@router.post("/overseas/order/market-buy")
async def place_overseas_market_buy(
    exchange_code: str,
    stock_code: str,
    quantity: Optional[int] = 0,  # 0이면 최대 수량으로 매수
    trading_service: TradingService = Depends(TradingService)
):
    """해외주식 시장가 매수 (최우선 매도호가 사용)"""
    try:
        # 호가 정보 조회
        hoga_info = trading_service.get_hoga_info_overseas(exchange_code, stock_code)
        if not hoga_info:
            raise HTTPException(status_code=404, detail="Failed to get hoga information")

        # 수량이 0이면 최대 매수 가능 수량 계산
        if quantity == 0:
            quantity = trading_service.calculate_overseas_max_buy_quantity(exchange_code, stock_code)
            if not quantity:
                raise HTTPException(status_code=400, detail="Failed to calculate max buy quantity")

        # 주문 실행
        result = trading_service.place_buy_order_overseas(
            exchange_code=exchange_code,
            stock_code=stock_code,
            price=hoga_info['ask_price'],
            quantity=quantity,
            order_type=OrderType.LIMIT
        )

        if not result:
            raise HTTPException(status_code=400, detail="Order failed")

        # result 객체에서 필요한 정보만 추출
        order_info = {
            "rt_cd": result.get_body().rt_cd,
            "msg_cd": result.get_body().msg_cd,
            "msg1": result.get_body().msg1,
            "output": result.get_body().output
        }

        return {
            "status": "success",
            "order_info": order_info,
            "quantity": quantity,
            "price": hoga_info['ask_price']
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in market buy: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 
    

@router.post("/overseas/order/market-sell")
async def place_overseas_market_sell(
    exchange_code: str,
    stock_code: str,
    quantity: Optional[int] = 0,  # 0이면 최대 수량으로 매도
    trading_service: TradingService = Depends(TradingService)
):
    """해외주식 시장가 매도 (최우선 매수호가 사용)"""
    try:
        # 호가 정보 조회
        hoga_info = trading_service.get_hoga_info_overseas(exchange_code, stock_code)
        if not hoga_info:
            raise HTTPException(status_code=404, detail="Failed to get hoga information")
        
        # 수량이 0이면 최대 매도 가능 수량 계산
        if not quantity:
            quantity = trading_service.calculate_overseas_max_sell_quantity(exchange_code, stock_code)
            if not quantity:
                raise HTTPException(status_code=400, detail="No holdings available for sell")

        # 주문 실행
        result = trading_service.place_sell_order_overseas(
            exchange_code=exchange_code,
            stock_code=stock_code,
            price=hoga_info['bid_price'],  # 최우선 매수호가
            quantity=quantity,
            order_type=OrderType.LIMIT  # 시장가 주문
        )

        if not result:
            raise HTTPException(status_code=400, detail="Order failed")

        # result 객체에서 필요한 정보만 추출
        order_info = {
            "rt_cd": result.get_body().rt_cd,
            "msg_cd": result.get_body().msg_cd,
            "msg1": result.get_body().msg1,
            "output": result.get_body().output
        }

        return {
            "status": "success",
            "order_info": order_info,
            "quantity": quantity,
            "price": hoga_info['bid_price']
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in market sell: {e}")
        raise HTTPException(status_code=500, detail=str(e))