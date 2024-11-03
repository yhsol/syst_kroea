from app.core.utils import KoreaInvestEnv, KoreaInvestAPI
from app.core.config import get_settings

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