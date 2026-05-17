from sqlalchemy import create_engine
from db.session import DATABASE_URL, SessionLocal
from services.auth import create_admin

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

if __name__ == "__main__":
    db = SessionLocal()

    try:
        create_admin(db=db, username=ADMIN_USERNAME, password=ADMIN_PASSWORD)
        print("Admin created successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()
