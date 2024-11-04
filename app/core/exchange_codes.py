from enum import Enum
from typing import Dict, Optional

class ExchangeCode(Enum):
    # 미국
    NASDAQ = "NASDAQ"
    NYSE = "NYSE"
    AMEX = "AMEX"
    # 아시아
    HONGKONG = "HONGKONG"
    SHANGHAI = "SHANGHAI"
    SHENZHEN = "SHENZHEN"
    TOKYO = "TOKYO"
    HANOI = "HANOI"
    HOCHIMINH = "HOCHIMINH"

class ExchangeCodeConverter:
    # API 엔드포인트별 거래소 코드 매핑
    MAPPING = {
        "HOGA": {  # 호가 조회용 (EXCD)
            ExchangeCode.NASDAQ: "NAS",
            ExchangeCode.NYSE: "NYS",
            ExchangeCode.AMEX: "AMS",
            ExchangeCode.HONGKONG: "HKS",
            ExchangeCode.SHANGHAI: "SHS",
            ExchangeCode.SHENZHEN: "SZS",
            ExchangeCode.TOKYO: "TSE",
            ExchangeCode.HANOI: "HNX",
            ExchangeCode.HOCHIMINH: "HSX",
        },
        "ORDER": {  # 주문용 (OVRS_EXCG_CD)
            ExchangeCode.NASDAQ: "NASD",
            ExchangeCode.NYSE: "NYSE",
            ExchangeCode.AMEX: "AMEX",
            ExchangeCode.HONGKONG: "SEHK",
            ExchangeCode.SHANGHAI: "SHAA",
            ExchangeCode.SHENZHEN: "SZAA",
            ExchangeCode.TOKYO: "TKSE",
            ExchangeCode.HANOI: "HASE",
            ExchangeCode.HOCHIMINH: "VNSE",
        },
        "BUYABLE": {  # 매수가능금액 조회용
            ExchangeCode.NASDAQ: "NASD",
            ExchangeCode.NYSE: "NYSE",
            ExchangeCode.AMEX: "AMEX",
            ExchangeCode.HONGKONG: "SEHK",
            ExchangeCode.SHANGHAI: "SHAA",
            ExchangeCode.SHENZHEN: "SZAA",
            ExchangeCode.TOKYO: "TKSE",
            ExchangeCode.HANOI: "HASE",
            ExchangeCode.HOCHIMINH: "VNSE",
        }
    }

    @classmethod
    def get_code(cls, exchange: ExchangeCode, api_type: str) -> Optional[str]:
        """
        거래소 코드 변환
        :param exchange: ExchangeCode Enum
        :param api_type: API 타입 ("HOGA" or "ORDER" or "BUYABLE")
        :return: 변환된 거래소 코드
        """
        return cls.MAPPING.get(api_type, {}).get(exchange)

    @classmethod
    def from_string(cls, exchange_str: str) -> Optional[ExchangeCode]:
        """
        문자열을 ExchangeCode Enum으로 변환
        """
        try:
            return ExchangeCode[exchange_str.upper()]
        except KeyError:
            return None 