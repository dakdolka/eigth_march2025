from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    token: str
    db_url: str = f'sqlite+aiosqlite:///{BASE_DIR}/data/db.db'
    
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")  
    
settings = Settings()
 
    
