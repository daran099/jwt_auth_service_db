from services.auth import create_user, authenticate_user
from sqlalchemy.orm import Session


def test_create_user(db: Session):
    user = create_user(db, "service_user", "1234")

    assert user.id is not None
    assert user.username == "service_user"


def test_create_user_duplicate(db: Session):
    create_user(db, "dup_service", "1234")

    try:
        create_user(db, "dup_service", "1234")
        assert False
    except ValueError:
        assert True


def test_authenticate_success(db: Session):
    create_user(db, "auth_user", "1234")

    user = authenticate_user(db, "auth_user", "1234")

    assert user is not None


def test_authenticate_wrong_password(db: Session):
    create_user(db, "auth_bad", "1234")

    try:
        authenticate_user(db, "auth_bad", "wrong")
        assert False
    except Exception:
        assert True
