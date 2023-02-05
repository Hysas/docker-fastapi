import pytest

from src import schemas


def test_get_all_posts(authorized_client, create_test_posts):
    response = authorized_client.get("/posts")
    def validate_schema(post):
        return schemas.PostOut(**post)
    posts_map = map(validate_schema, response.json())
    # posts_list = list(posts_map)
    assert len(response.json()) == len(create_test_posts)
    assert response.status_code == 200

def test_unauth_get_all_posts(client, create_test_posts):
    response = client.get("/posts")
    assert response.status_code == 401

def test_unauth_get_one_post(client, create_test_posts):
    response = client.get(f"/posts/{create_test_posts[0].id}")
    assert response.status_code == 401

def test_get_get_one_post_not_exist(authorized_client, create_test_posts):
    response = authorized_client.get(f"/posts/8888")
    assert response.status_code == 404

def test_get_one_post(authorized_client, create_test_posts):
    response = authorized_client.get(f"/posts/{create_test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert response.status_code == 200
    assert post.Post.id == create_test_posts[0].id
    assert post.Post.content == create_test_posts[0].content
    assert post.Post.title == create_test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("Title1", "Content1", True),
    ("Title1", "Content1", False),
    ("Title2", "Content2", False),
    ("Title2", "Content2", True),
    ("Title3", "Content3", False),
    ("Title3", "Content3", True),
])
def test_create_post(authorized_client, create_test_user, create_test_posts, title, content, published):
    response = authorized_client.post("/posts", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == create_test_user["id"]

def test_create_post_published_default_true(authorized_client, create_test_user, create_test_posts):
    response = authorized_client.post("/posts", json={"title": "testtitle", "content": "testcontent"})
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == "testtitle"
    assert created_post.content == "testcontent"
    assert created_post.published == True
    assert created_post.owner_id == create_test_user["id"]

def test_unauth_create_post(client, create_test_user, create_test_posts):
    response = client.post("/posts", json={"title": "testtitle", "content": "testcontent"})
    assert response.status_code == 401

def test_unauth_delete_post(client, create_test_user, create_test_posts):
    response = client.delete(f"/posts/{create_test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post_successfull(authorized_client, create_test_user, create_test_posts):
    response = authorized_client.delete(f"/posts/{create_test_posts[0].id}")
    assert response.status_code == 204

def test_delete_post_nonexist(authorized_client, create_test_user, create_test_posts):
    response = authorized_client.delete(f"/posts/100000")
    assert response.status_code == 404

def test_delete_other_user_post(authorized_client, create_test_user, create_test_posts):
    response = authorized_client.delete(f"/posts/{create_test_posts[3].id}")
    assert response.status_code == 401

def test_update_post(authorized_client, create_test_user, create_test_posts):
    data = {
        "title": "updated title",
        "content": "updated content"
    }
    response = authorized_client.put(f"/posts/{create_test_posts[0].id}", json=data)
    post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert post.id == create_test_posts[0].id
    assert post.content == data["content"]
    assert post.title == data["title"]

def test_update_other_user_post(authorized_client, create_test_user, create_test_user2, create_test_posts):
    data = {
        "title": "updated title",
        "content": "updated content"
    }
    response = authorized_client.put(f"/posts/{create_test_posts[3].id}", json=data)
    assert response.status_code == 401


def test_update_post_unauth(client, create_test_user, create_test_posts):
    data = {
        "title": "updated title",
        "content": "updated content"
    }
    response = client.put(f"/posts/{create_test_posts[0].id}", json=data)
    assert response.status_code == 401  

def test_update_post_nonexist(authorized_client, create_test_user, create_test_posts):
    data = {
        "title": "updated title",
        "content": "updated content"
    }
    response = authorized_client.put(f"/posts/100000", json=data)
    assert response.status_code == 404