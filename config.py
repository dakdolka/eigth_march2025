from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram import Bot


BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    token: str
    group_id: int = -1002467822218
    not_approved_thread_id: int = 5
    approved_thread_id: int = 12
    db_url: str = f'sqlite+aiosqlite:///{BASE_DIR}/data/db.db'
    
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")  
    
settings = Settings()
 

BOT = Bot(token=settings.token)
