from fastapi import APIRouter, Request, HTTPException
from app.core.constants import OrderType
from app.services.trading_service import TradingService
from app.models.webhook import TradingViewAlert
import logging

# 로거 생성
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/tradingview")
async def tradingview_webhook(request: Request):
    try:
        # 요청 본문 파싱
        body = await request.json()
        logger.info(f"Received webhook data: {body}")
        
        # 데이터 검증
        alert = TradingViewAlert(**body)
        logger.info(f"Parsed alert data: {alert}")
        
        # 트레이딩 로직 실행
        trading_service = TradingService()
        
        # 주문 파라미터 로깅
        logger.info(f"Placing order: timeframe={alert.timeframe}, symbol={alert.symbol}, quantity={alert.quantity}, "
                    f"price={alert.price}, order_type={alert.order_type}, market={alert.market}")
        
        # market에 따라 주문 실행
        # if alert.market == "korea":
        #     if alert.action == "buy":
        #         result = trading_service.place_buy_order(
        #             alert.symbol,
        #             alert.quantity,
        #             int(alert.price),
        #             alert.order_type
        #         )
        #     elif alert.action == "sell":
        #         result = trading_service.place_sell_order(
        #             alert.symbol,
        #             alert.quantity,
        #             int(alert.price),
        #             alert.order_type
        #         )
        # else:
        #     if alert.action == "buy":
        #         result = trading_service.place_buy_order_overseas(
        #             "NASD",
        #             alert.symbol,
        #             0,
        #             1,
        #             OrderType.LIMIT
        #         )
        #     elif alert.action == "sell":
        #         result = trading_service.place_sell_order_overseas(
        #             "NASD",
        #             alert.symbol,
        #             0,
        #             1,
        #             OrderType.LIMIT
        #         )
        result = '' # 실제 거래 시작시 제거


        logger.info(f"Order result: {result}")
        return {"status": "success", "data": result}

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 