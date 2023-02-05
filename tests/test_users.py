import pytest
from jose import jwt

from src import schemas, config


def test_create_user(client):
    test_email = "testuser@testdomain.com"
    test_password = "password123"
    response = client.post("/users", json={"email":test_email, "password": test_password})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == test_email
    assert response.status_code == 201

def test_login_user(client, create_test_user):
    response = client.post("/login", data={"username":create_test_user["email"], "password": create_test_user["password"]})
    new_login = schemas.Token(**response.json())
    payload = jwt.decode(new_login.access_token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM])
    id = payload.get("user_id")
    assert create_test_user["id"] == id
    assert new_login.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("testuser@testdomain.com", "Wrong Password", 403),
    ("Wrong Email", "password123", 403),
    ("Wrong Email", "Wrong Password", 403),
    (None, "password123", 422),
    ("testuser@testdomain.com", None, 422),
    (None, None, 422)
])
def test_incorrect_login(client, create_test_user, email, password, status_code):
    response = client.post("/login", data={"username":email, "password": password})
    assert response.status_code == status_code
    # assert response.json().get('detail') == "Invalid credentials"

# def test_incorrect_login(client, create_test_user):
#     response = client.post("/login", data={"username":create_test_user["email"], "password": "GAH"})
#     assert response.status_code == 403
#     assert response.json().get('detail') == "Invalid credentials"