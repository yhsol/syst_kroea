from datetime import datetime, timedelta
import json
import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class TokenManager:
    _instance: Optional['TokenManager'] = None
    _initialized: bool = False
    
    def __new__(cls, api_key: str = "", api_secret: str = ""):
        if cls._instance is None:
            cls._instance = super(TokenManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_key: str = "", api_secret: str = ""):
        if not TokenManager._initialized:
            self.api_key = api_key
            self.api_secret = api_secret
            self.token = None
            self.expires_at = None
            
            if api_key and api_secret:  # credentials가 제공된 경우에만 토큰 발급
                self._issue_new_token()
                TokenManager._initialized = True

    def initialize(self, api_key: str, api_secret: str):
        """TokenManager 초기화 (credentials 설정)"""
        if not TokenManager._initialized:
            self.api_key = api_key
            self.api_secret = api_secret
            self._issue_new_token()
            TokenManager._initialized = True

    def _issue_new_token(self):
        """새로운 토큰 발급"""
        if not self.api_key or not self.api_secret:
            raise ValueError("API credentials not set")
            
        if not self.token or not self.expires_at or \
           self.expires_at - timedelta(hours=1) <= datetime.now():
            
            url = "https://openapi.koreainvestment.com:9443/oauth2/tokenP"
            headers = {"content-type": "application/json"}
            body = {
                "grant_type": "client_credentials",
                "appkey": self.api_key,
                "appsecret": self.api_secret
            }
            
            try:
                res = requests.post(url, headers=headers, data=json.dumps(body))
                res.raise_for_status()
                
                token_data = res.json()
                self.token = token_data.get('access_token')
                self.expires_at = datetime.now() + timedelta(hours=24)
                logger.info("Issued new token")
                
            except Exception as e:
                logger.error(f"Error issuing new token: {e}")
                raise

    def get_token(self) -> str:
        """유효한 토큰 반환"""
        if not TokenManager._initialized:
            raise ValueError("TokenManager not initialized")
            
        self._issue_new_token()  # 필요한 경우에만 새로운 토큰 발급
        return f"Bearer {self.token}"