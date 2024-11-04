from fastapi import APIRouter, Request, HTTPException
from app.core.constants import OrderType
from app.services.trading_service import TradingService
from app.models.webhook import TradingViewAlert
from app.core.exchange_codes import ExchangeCodeConverter
import logging

# 로거 생성
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/tradingview")
async def tradingview_webhook(request: Request):
    try:
        body = await request.json()
        logger.info(f"Received webhook data: {body}")
        
        # 데이터 검증
        alert = TradingViewAlert(**body)
        logger.info(f"Parsed alert data: {alert}")
        
        # 트레이딩 로직 실행
        trading_service = TradingService()
        
        # TradingView exchange 코드를 내부 코드로 변환
        exchange = ExchangeCodeConverter.from_tradingview(alert.exchange)
        if not exchange:
            raise ValueError(f"Invalid exchange code from TradingView: {alert.exchange}")
        
        upper_exchange_code = exchange.name
        upper_symbol = alert.symbol.upper()
        
        # 주문 파라미터 로깅
        logger.info(f"Placing order: timeframe={alert.timeframe}, symbol={upper_symbol}, "
                   f"exchange={upper_exchange_code}, quantity={alert.quantity}")
        
        # market에 따라 주문 실행
        if alert.market == "korea":
            # 기존 국내 주식 로직
            pass
        else:  # Overseas market
            # 호가 정보 조회
            hoga_info = trading_service.get_hoga_info_overseas(upper_exchange_code, upper_symbol)
            if not hoga_info:
                raise HTTPException(status_code=404, detail="Failed to get hoga information")

            if alert.action == "buy":
                # 수량이 0이면 최대 매수 가능 수량 계산
                quantity = alert.quantity if alert.quantity > 0 else trading_service.calculate_overseas_max_buy_quantity(
                    upper_exchange_code,
                    upper_symbol
                )
                
                if not quantity:
                    raise HTTPException(status_code=400, detail="Failed to calculate buy quantity")

                # 매수 주문 실행
                result = trading_service.place_buy_order_overseas(
                    exchange_code=upper_exchange_code,
                    stock_code=upper_symbol,
                    price=hoga_info['ask_price'],
                    quantity=quantity,
                    order_type=OrderType.LIMIT
                )

            elif alert.action == "sell":
                # 수량이 0이면 최대 매도 가능 수량 계산
                quantity = alert.quantity if alert.quantity > 0 else trading_service.calculate_overseas_max_sell_quantity(
                    upper_exchange_code,
                    upper_symbol
                )
                
                if not quantity:
                    raise HTTPException(status_code=400, detail="No holdings available for sell")

                # 매도 주문 실행
                result = trading_service.place_sell_order_overseas(
                    exchange_code=upper_exchange_code,
                    stock_code=upper_symbol,
                    price=hoga_info['bid_price'],
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
                "price": hoga_info['ask_price'] if alert.action == "buy" else hoga_info['bid_price']
            }

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 