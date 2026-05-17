from sqlalchemy import select

from models import User, RefreshToken


def test_register_creates_user(client, db):
    client.post("/register", json={"username": "db_user", "password": "1234"})

    stmt = select(User).where(User.username == "db_user")
    user = db.execute(stmt).scalar_one_or_none()

    assert user is not None
    assert user.username == "db_user"


def test_register_success(client):
    res = client.post("/register", json={"username": "user1", "password": "1234"})

    assert res.status_code == 200
    assert res.json()["username"] == "user1"


def test_register_duplicate(client):
    client.post("/register", json={"username": "dup", "password": "123"})

    res = client.post("/register", json={"username": "dup", "password": "123"})

    assert res.status_code == 400


def test_login_success(client):
    client.post("/register", json={"username": "login", "password": "1234"})

    res = client.post("/login", json={"username": "login", "password": "1234"})

    assert res.status_code == 200
    data = res.json()

    assert "access_token" in data
    assert res.cookies.get("refresh_token") is not None


def test_login_wrong_password(client):
    client.post("/register", json={"username": "bad", "password": "1234"})

    res = client.post("/login", json={"username": "bad", "password": "wrong"})

    assert res.status_code == 401


def test_login_user_not_found(client):
    res = client.post("/login", json={"username": "ghost", "password": "123"})

    assert res.status_code == 401


def test_access_token_works(client):
    client.post("/register", json={"username": "secure", "password": "1234"})

    login = client.post("/login", json={"username": "secure", "password": "1234"})

    token = login.json()["access_token"]

    res = client.get("/me", headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 200
    assert res.json()["username"] == "secure"


def test_access_without_token(client):
    res = client.get("/me")
    assert res.status_code == 403 or res.status_code == 401


def test_access_with_invalid_token(client):
    res = client.get("/me", headers={"Authorization": "Bearer invalid"})

    assert res.status_code == 401


def test_refresh_token_saved_in_db(client, db):
    client.post("/register", json={"username": "token_user", "password": "1234"})

    res = client.post("/login", json={"username": "token_user", "password": "1234"})

    refresh_cookie = res.cookies.get("refresh_token")

    stmt = select(RefreshToken).where(RefreshToken.token == refresh_cookie)

    token = db.execute(stmt).scalar_one_or_none()

    assert token is not None


def test_refresh_success(client):
    client.post("/register", json={"username": "refresh", "password": "1234"})

    login = client.post("/login", json={"username": "refresh", "password": "1234"})

    refresh_token = login.cookies.get("refresh_token")

    res = client.post("/refresh", cookies={"refresh_token": refresh_token})

    assert res.status_code == 200
    data = res.json()

    assert "access_token" in data


def test_refresh_invalid_token(client):
    res = client.post("/refresh", cookies={"refresh_token": "fake"})

    assert res.status_code == 401


def test_logout_deletes_refresh_token(client, db):
    client.post("/register", json={"username": "logout_db", "password": "1234"})

    login = client.post("/login", json={"username": "logout_db", "password": "1234"})

    refresh_token = login.cookies.get("refresh_token")

    client.post("/logout", cookies={"refresh_token": refresh_token})

    stmt = select(RefreshToken).where(RefreshToken.token == refresh_token)

    token = db.execute(stmt).scalar_one_or_none()

    assert token is None


def test_logout(client):
    client.post("/register", json={"username": "logout", "password": "1234"})

    login = client.post("/login", json={"username": "logout", "password": "1234"})

    refresh_token = login.cookies.get("refresh_token")

    res = client.post("/logout", cookies={"refresh_token": refresh_token})

    assert res.status_code == 200

    res2 = client.post("/refresh", cookies={"refresh_token": refresh_token})

    assert res2.status_code == 401
