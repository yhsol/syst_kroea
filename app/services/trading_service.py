from app.core.utils import KoreaInvestEnv, KoreaInvestAPI
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

class TradingService:
    def __init__(self):
        settings = get_settings()
        self.config = {
            "api_key": settings.API_KEY,
            "api_secret_key": settings.API_SECRET_KEY,
            "stock_account_number": settings.STOCK_ACCOUNT_NUMBER,
            "stock_account_product_code": settings.STOCK_ACCOUNT_PRODUCT_CODE,
            "hts_id": settings.HTS_ID,
            "custtype": settings.CUSTTYPE,
            "is_paper_trading": settings.IS_PAPER_TRADING,
            "my_agent": settings.MY_AGENT,
            "url": settings.URL,
            "webhook_url": settings.WEBHOOK_URL
        }
        self.env = KoreaInvestEnv(self.config)
        self.api = KoreaInvestAPI(self.env.get_full_config(), self.env.get_base_headers())

    def get_balance(self):
        return self.api.get_account_balance("")

    def get_current_price(self, stock_code: str):
        return self.api.get_current_price(stock_code)

    def get_hoga_info(self, stock_code: str):
        return self.api.get_hoga_info(stock_code)

    def get_fluctuation_rank(self):
        return self.api.get_fluctuation_rank()

    def place_buy_order(self, stock_code: str, quantity: int, price: float, order_type: str):
        return self.api.do_buy_order(stock_code, quantity, price, order_type)

    def place_sell_order(self, stock_code: str, quantity: int, price: float, order_type: str):
        return self.api.do_sell_order(stock_code, quantity, price, order_type)

    def get_orders(self):
        return self.api.get_orders()

    def cancel_order(self, order_no: str, quantity: int, price: str):
        return self.api.do_cancel_order(order_no, quantity, price)

    def get_current_price_overseas(self, exchange_code: str, stock_code: str):
        return self.api.get_current_price_overseas(exchange_code, stock_code)

    def get_balance_overseas(self):
        return self.api.get_account_balance_overseas()

    def place_buy_order_overseas(self, exchange_code: str, stock_code: str, price: float, quantity: int, order_type: str = "00"):
        return self.api.do_buy_order_overseas(exchange_code, stock_code, price, quantity, order_type)

    def place_sell_order_overseas(self, exchange_code: str, stock_code: str, price: float, quantity: int, order_type: str = "00"):
        return self.api.do_sell_order_overseas(exchange_code, stock_code, price, quantity, order_type) 
    
    # 호가
    def get_hoga_info_overseas(self, exchange_code: str, stock_code: str):
        return self.api.get_hoga_info_overseas(exchange_code, stock_code)
    
    # 매수가능금액
    def get_buyable_amount_overseas(self, exchange_code: str, stock_code: str, price: float):
        return self.api.get_buyable_amount_overseas(exchange_code, stock_code, price)

    # 최대 매수 가능 수량 계산
    def calculate_overseas_max_buy_quantity(self, exchange_code: str, stock_code: str) -> int:
        """해외주식 최대 매수 가능 수량 계산"""
        try:
            # 1. 호가 정보 조회
            hoga_info = self.get_hoga_info_overseas(exchange_code, stock_code)
            if not hoga_info:
                logger.error("Failed to get overseas hoga info")
                return 0
                
            # 2. 매수가능금액 조회 (최우선 매도호가 기준)
            buyable_info = self.get_buyable_amount_overseas(
                exchange_code, 
                stock_code, 
                hoga_info['ask_price']
            )
            
            if not buyable_info:
                logger.error("Failed to get overseas buyable amount")
                return 0
                
            # 3. 최대 매수 가능 수량 반환 (통합 기준)
            max_quantity = buyable_info['max_quantity']
            logger.info(f"Calculated max buy quantity: {max_quantity}")
            return max_quantity
            
        except Exception as e:
            logger.error(f"Error calculating overseas max buy quantity: {e}")
            return 0

    def calculate_overseas_max_sell_quantity(self, exchange_code: str, stock_code: str) -> int:
        """해외주식 최대 매도 가능 수량 계산"""
        try:
            # 잔고 조회
            _, holdings = self.get_balance_overseas()

            upper_exchange_code = exchange_code.upper()
            upper_stock_code = stock_code.upper()
            
            # 해당 종목 찾기
            target_holding = holdings[
                (holdings['해외거래소코드'] == upper_exchange_code) & 
                (holdings['종목코드'] == upper_stock_code)
            ]
            
            if target_holding.empty:
                logger.error(f"No holding found for {upper_exchange_code}:{upper_stock_code}")
                return 0
                
            # 매도가능수량 반환
            quantity = int(target_holding.iloc[0]['매도가능수량'])
            logger.info(f"Calculated max sell quantity: {quantity}")
            return quantity
                
        except Exception as e:
            logger.error(f"Error calculating overseas max sell quantity: {e}")
            return 0