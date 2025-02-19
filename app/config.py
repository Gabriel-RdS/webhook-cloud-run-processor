import os
from typing import List
from app.utils.security import get_secret
from dotenv import load_dotenv

load_dotenv()

class Config:
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    PROJECT_ID = os.getenv("PROJECT_ID")
    INSIDER_API_TOKEN = get_secret("INSIDER_API_TOKEN", PROJECT_ID)
    ALLOWED_IPS: List[str] = [
        ip.strip() 
        for ip in os.getenv("ALLOWED_IPS", "").split(",") 
        if ip.strip()
    ]
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
