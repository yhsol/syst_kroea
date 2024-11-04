from datetime import datetime, timedelta
import json
import requests
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class TokenManager:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token_file = Path("token_cache.json")
        self.token = None
        self.expires_at = None
        self._load_cached_token()

    def _load_cached_token(self):
        """캐시된 토큰 정보 로드"""
        if self.token_file.exists():
            try:
                with open(self.token_file, 'r') as f:
                    data = json.load(f)
                    expires_at = datetime.fromisoformat(data['expires_at'])
                    
                    # 만료 1시간 전부터는 새로운 토큰 발급
                    if expires_at - timedelta(hours=1) > datetime.now():
                        self.token = data['token']
                        self.expires_at = expires_at
                        logger.info("Loaded cached token")
                        return
            except Exception as e:
                logger.error(f"Error loading cached token: {e}")
        
        self._issue_new_token()

    def _save_token_cache(self):
        """토큰 정보 캐시 저장"""
        try:
            with open(self.token_file, 'w') as f:
                json.dump({
                    'token': self.token,
                    'expires_at': self.expires_at.isoformat()
                }, f)
            logger.info("Saved token cache")
        except Exception as e:
            logger.error(f"Error saving token cache: {e}")

    def _issue_new_token(self):
        """새로운 토큰 발급"""
        url = "https://openapi.koreainvestment.com:9443/oauth2/tokenP"
        headers = {
            "content-type": "application/json"
        }
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
            
            self._save_token_cache()
            logger.info("Issued new token")
            
        except Exception as e:
            logger.error(f"Error issuing new token: {e}")
            raise

    def get_token(self) -> str:
        """유효한 토큰 반환"""
        if not self.token or not self.expires_at or \
           self.expires_at - timedelta(hours=1) <= datetime.now():
            self._issue_new_token()
        return f"Bearer {self.token}"  # Bearer 접두어 추가