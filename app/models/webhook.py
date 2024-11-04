from pydantic import BaseModel
from typing import Optional

class TradingViewAlert(BaseModel):
    timeframe: str
    action: str  # "buy" or "sell"
    symbol: str  # 종목 코드
    quantity: int
    price: float
    order_type: str = "01"  # 기본값은 지정가
    market: Optional[str] = None
    exchange_code: Optional[str] = "NASD"  # 해외주식 거래소 코드