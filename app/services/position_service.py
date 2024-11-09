from app.services.trading_service import TradingService
import logging
import math

logger = logging.getLogger(__name__)

class PositionService:
    def __init__(self):
        self.trading_service = TradingService()

    def reduce_all_positions(self, reduction_ratio: float = 0.5):
        """모든 해외 주식 포지션을 지정된 비율만큼 줄입니다.
        
        Args:
            reduction_ratio (float): 줄일 비율 (0.5는 50% 매도, 1.0은 전량 매도)
        """
        try:
            # 현재 보유 중인 포지션 조회
            _, holdings = self.trading_service.get_balance_overseas()
            
            if holdings.empty:
                logger.info("No positions to reduce")
                return {"status": "success", "message": "No positions to reduce"}

            results = []
            
            for _, position in holdings.iterrows():
                try:
                    exchange_code = position['해외거래소코드']
                    stock_code = position['종목코드']
                    current_quantity = int(position['보유수량'])
                    
                    # 매도할 수량 계산 (올림)
                    quantity_to_sell = math.ceil(current_quantity * reduction_ratio)
                    
                    if quantity_to_sell == 0:
                        continue

                    # 호가 정보 조회
                    hoga_info = self.trading_service.get_hoga_info_overseas(
                        exchange_code, 
                        stock_code
                    )
                    
                    if not hoga_info:
                        logger.error(f"Failed to get hoga info for {stock_code}")
                        continue

                    # 시장가 매도 주문 실행
                    result = self.trading_service.place_sell_order_overseas(
                        exchange_code=exchange_code,
                        stock_code=stock_code,
                        price=hoga_info['bid_price'],
                        quantity=quantity_to_sell
                    )

                    order_info = {
                        "exchange_code": exchange_code,
                        "stock_code": stock_code,
                        "sell_quantity": quantity_to_sell,
                        "price": hoga_info['bid_price'],
                        "status": "success" if result else "failed"
                    }
                    results.append(order_info)
                    
                except Exception as e:
                    logger.error(f"Error reducing position for {stock_code}: {str(e)}")
                    results.append({
                        "exchange_code": exchange_code,
                        "stock_code": stock_code,
                        "status": "failed",
                        "error": str(e)
                    })

            return {
                "status": "success",
                "orders": results
            }

        except Exception as e:
            logger.error(f"Error in reduce_all_positions: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            } 