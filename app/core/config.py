import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

def get_settings() -> Dict:
    """환경 변수에서 설정 값을 읽어옵니다."""
    return {
        "API_KEY": os.getenv("API_KEY"),
        "API_SECRET_KEY": os.getenv("API_SECRET_KEY"),
        "STOCK_ACCOUNT_NUMBER": os.getenv("STOCK_ACCOUNT_NUMBER"),
        "STOCK_ACCOUNT_PRODUCT_CODE": os.getenv("STOCK_ACCOUNT_PRODUCT_CODE", "01"),
        "HTS_ID": os.getenv("HTS_ID"),
        "CUSTTYPE": os.getenv("CUSTTYPE"),
        "IS_PAPER_TRADING": os.getenv("IS_PAPER_TRADING", "true").lower() == "true",
        "URL": os.getenv("URL"),
        "WEBHOOK_URL": os.getenv("WEBHOOK_URL"),
        "MY_AGENT": os.getenv("MY_AGENT")
    } 