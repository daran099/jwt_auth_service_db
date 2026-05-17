import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
REFRESH_EXPIRE_DAYS = int(os.getenv("REFRESH_EXPIRE_DAYS", 7))

DATABASE_URL = os.getenv("DATABASE_URL")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
