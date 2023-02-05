import pytest

from src import models

@pytest.fixture
def test_vote(session, create_test_user, create_test_posts):
    vote = models.Vote(post_id=create_test_posts[3].id, user_id=create_test_user["id"])
    session.add(vote)
    session.commit()

def test_vote_on_post(authorized_client, create_test_posts):
    data = {
        "post_id": create_test_posts[3].id,
        "dir": 1
    }
    response = authorized_client.post("/votes", json=data)
    assert response.status_code == 201

def test_vote_twice_post(authorized_client, test_vote, create_test_posts):
    data = {
        "post_id": create_test_posts[3].id,
        "dir": 1
    }
    response = authorized_client.post("/votes", json=data)
    assert response.status_code == 409

def test_delete_vote(authorized_client, create_test_posts, test_vote):
    data = {
        "post_id": create_test_posts[3].id,
        "dir": 0
    }
    response = authorized_client.post("/votes", json=data)
    assert response.status_code == 201

def test_delete_vote_nonexist(authorized_client, create_test_posts):
    data = {
        "post_id": create_test_posts[3].id,
        "dir": 0
    }
    response = authorized_client.post("/votes", json=data)
    assert response.status_code == 404

def test_vote_post_nonexist(authorized_client, create_test_posts):
    data = {
        "post_id": 100000,
        "dir": 1
    }
    response = authorized_client.post("/votes", json=data)
    assert response.status_code == 404 

def test_vote_on_post_unauth(client, create_test_posts):
    data = {
        "post_id": create_test_posts[3].id,
        "dir": 1
    }
    response = client.post("/votes", json=data)
    assert response.status_code == 401