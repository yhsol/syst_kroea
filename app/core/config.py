import yaml
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    config_path: str = "config.yaml"

    @property
    def trading_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

@lru_cache()
def get_settings():
    return Settings() 