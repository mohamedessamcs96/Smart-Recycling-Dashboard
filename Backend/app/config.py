# app/config.py
from pydantic import BaseSettings   
import os 
class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    UPLOAD_DIR: str = os.path.join(os.getcwd(), "uploads")


    class Config:
        env_file = ".env"

settings = Settings()
