from fastapi import APIRouter, Request
from app.services.trading_service import TradingService
from app.models.webhook import TradingViewAlert

router = APIRouter()

@router.post("/tradingview")
async def tradingview_webhook(alert: TradingViewAlert):
    print("alert: ", alert)
    trading_service = TradingService()
    
    # 트레이딩뷰로부터 받은 시그널에 따라 주문 실행
    # if alert.action == "buy":
    #     result = trading_service.place_buy_order(
    #         alert.symbol,
    #         alert.quantity,
    #         alert.price,
    #         alert.order_type
    #     )
    # elif alert.action == "sell":
    #     result = trading_service.place_sell_order(
    #         alert.symbol,
    #         alert.quantity,
    #         alert.price,
    #         alert.order_type
    #     )
    
    return {"status": "success", "data": result} 