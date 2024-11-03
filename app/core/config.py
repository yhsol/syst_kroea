from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    API_KEY: str
    API_SECRET_KEY: str
    
    # Account Info
    STOCK_ACCOUNT_NUMBER: str
    STOCK_ACCOUNT_PRODUCT_CODE: str
    HTS_ID: str
    CUSTTYPE: str
    IS_PAPER_TRADING: bool
    
    # Service URLs
    URL: str
    WEBHOOK_URL: str
    
    # User Agent
    MY_AGENT: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings() 