import pytest
# import requests
# from urllib.parse import urljoin
# from urllib3.util.retry import Retry
# from requests.adapters import HTTPAdapter
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base   

from src import config, models, oauth2
from src.main import app
from src.database import get_db

# pytest_plugins = ["docker_compose"]


NODE_ENV = config.settings.NODE_ENV
DB_HOST = config.settings.DB_HOST
DB_PORT = config.settings.DB_PORT
DB_USER = config.settings.DB_USER
DB_PASSWORD = config.settings.DB_USER
DB_NAME = config.settings.DB_NAME + "_test"

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="function")
# def wait_for_api(function_scoped_container_getter):
#     """Wait for the api from my_api_service to become responsive"""
#     request_session = requests.Session()
#     retries = Retry(total=5,
#                     backoff_factor=0.1,
#                     status_forcelist=[500, 502, 503, 504])
#     request_session.mount('http://', HTTPAdapter(max_retries=retries))

#     service = function_scoped_container_getter.get("my_api_service").network_info[0]
#     api_url = "http://%s:%s/" % (service.hostname, service.host_port)
#     assert request_session.get(api_url)
#     return request_session, api_url

# def test_read_and_write(wait_for_api):
#     """The Api is now verified good to go and tests can interact with it"""
#     request_session, api_url = wait_for_api
#     data_string = 'some_data'
#     request_session.put('%sitems/2?data_string=%s' % (api_url, data_string))
#     item = request_session.get(urljoin(api_url, 'items/2')).json()
#     assert item['data'] == data_string
#     request_session.delete(urljoin(api_url, 'items/2'))

@pytest.fixture
def session():    
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)
    # Code after run

@pytest.fixture
def create_test_user2(client):
    test_email = "testuser2@testdomain.com"
    test_password = "password123"
    user_data = {"email":test_email, "password": test_password}
    response = client.post("/users", json=user_data)
    new_user = response.json()
    new_user["password"] = test_password
    assert response.status_code == 201
    return new_user

@pytest.fixture
def create_test_user(client):
    test_email = "testuser@testdomain.com"
    test_password = "password123"
    user_data = {"email":test_email, "password": test_password}
    response = client.post("/users", json=user_data)
    new_user = response.json()
    new_user["password"] = test_password
    assert response.status_code == 201
    return new_user

@pytest.fixture
def token(create_test_user):
    return oauth2.create_access_token({"user_id": create_test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def create_test_posts(create_test_user, create_test_user2, session):
    posts_data = [
        {
            "title": "1st title",
            "content": "1st content",
            "owner_id": create_test_user["id"]
        },
        {
            "title": "2st title",
            "content": "2st content",
            "owner_id": create_test_user["id"]
        },
        {
            "title": "3st title",
            "content": "3st content",
            "owner_id": create_test_user["id"]
        },
        {
            "title": "4st title",
            "content": "4st content",
            "owner_id": create_test_user2["id"]
        }
        
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts_list = list(post_map)

    session.add_all(posts_list)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
