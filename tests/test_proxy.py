"""Tests proxy.py.

This test file contains all Flask tests; other components, e.g., the GraphQL
schema, are tested in isolation of Flask.
"""

import json
from flask import url_for
from flask.testing import FlaskClient
from populare_db_proxy.app_data import db


def test_get_health_endpoint_gives_ok_code(client: FlaskClient) -> None:
    """Tests that a GET request on the health endpoint gives code 200.

    :param client: The flask client.
    """
    assert client.get(url_for('health')).status_code == 200


def test_get_graphql_endpoint_gives_bad_response_code(
        client: FlaskClient
) -> None:
    """Tests that a GET request on the graphql endpoint gives code 400.

    :param client: The flask client.
    """
    assert client.get(url_for('graphql')).status_code == 400


def test_post_graphql_endpoint_gives_ok_code(client: FlaskClient) -> None:
    """Tests that a POST request on the graphql endpoint gives code 200.

    :param client: The flask client.
    """
    assert client.post(
        url_for('graphql'),
        data="{ initDb }",
        content_type="application/graphql"
    ).status_code == 200


def test_resolve_init_db_responds_ok(client: FlaskClient) -> None:
    """Tests that a POST request on initDb responds ok.

    :param client: The flask client.
    """
    db.drop_all()
    response = client.post(
        url_for('graphql'),
        data="{ initDb }",
        content_type="application/graphql"
    )
    assert response.status_code == 200
    content = json.loads(response.text)
    assert content["data"]["initDb"] == "ok"


def test_resolve_read_posts_no_db_fails(client: FlaskClient) -> None:
    """Tests that a POST request on readPosts fails when the database has not
    been initialized.

    :param client: The flask client.
    """
    db.drop_all()
    response = client.post(
        url_for('graphql'),
        data="{ readPosts }",
        content_type="application/graphql"
    )
    assert response.status_code == 200
    content = json.loads(response.text)
    assert "errors" in content
    assert "no such table" in content["errors"][0]["message"]


def test_resolve_read_posts_empty_db_returns_empty_list(
        client: FlaskClient
) -> None:
    """Tests that a POST request on readPosts returns the empty list when the
    database is empty.

    :param client: The flask client.
    """
    db.drop_all()
    _ = client.post(
        url_for('graphql'),
        data="{ initDb }",
        content_type="application/graphql"
    )
    response = client.post(
        url_for('graphql'),
        data="{ readPosts }",
        content_type="application/graphql"
    )
    assert response.status_code == 200
    content = json.loads(response.text)
    assert content["data"]["readPosts"] == []


def test_resolve_read_posts_returns_posts(client: FlaskClient) -> None:
    """Tests that a POST request on readPosts returns a list of posts.

    :param client: The flask client.
    """
    db.drop_all()
    _ = client.post(
        url_for('graphql'),
        data="{ initDb }",
        content_type="application/graphql"
    )
    _ = client.post(
        url_for('graphql'),
        data="""
        {
            createPost
            (
                text: "my text",
                author: "my author",
                createdAt: "2006-01-02T15:04:05"
            )
        }
        """,
        content_type="application/graphql"
    )
    response = client.post(
        url_for('graphql'),
        data="{ readPosts }",
        content_type="application/graphql"
    )
    assert response.status_code == 200
    content = json.loads(response.text)
    posts = [json.loads(post) for post in content["data"]["readPosts"]]
    assert len(posts) == 1
    assert posts[0]["text"] == "my text"


def test_resolve_create_post_returns_post(client: FlaskClient) -> None:
    """Tests that a POST request on createPost returns the input post.

    :param client: The flask client.
    """
    db.drop_all()
    _ = client.post(
        url_for('graphql'),
        data="{ initDb }",
        content_type="application/graphql"
    )
    response = client.post(
        url_for('graphql'),
        data="""
        {
            createPost
            (
                text: "my text",
                author: "my author",
                createdAt: "2006-01-02T15:04:05"
            )
        }
        """,
        content_type="application/graphql"
    )
    assert response.status_code == 200
    content = json.loads(response.text)
    post = json.loads(content["data"]["createPost"])
    assert post["text"] == "my text"


def test_resolve_update_post_returns_post(client: FlaskClient) -> None:
    """Tests that a POST request on updatePost returns the input post.

    :param client: The flask client.
    """
    db.drop_all()
    _ = client.post(
        url_for('graphql'),
        data="{ initDb }",
        content_type="application/graphql"
    )
    _ = client.post(
        url_for('graphql'),
        data="""
        {
            createPost
            (
                text: "my text",
                author: "my author",
                createdAt: "2006-01-02T15:04:05"
            )
        }
        """,
        content_type="application/graphql"
    )
    response = client.post(
        url_for('graphql'),
        data="""
        {
            updatePost
            (
                postId: 1,
                text: "new text",
                author: "new author",
                createdAt: "2006-01-02T15:04:05"
            )
        }
        """,
        content_type="application/graphql"
    )
    assert response.status_code == 200
    content = json.loads(response.text)
    post = json.loads(content["data"]["updatePost"])
    assert post["text"] == "new text"


def test_resolve_delete_post_returns_ok(client: FlaskClient) -> None:
    """Tests that a POST request on deletePost returns ok.

    :param client: The flask client.
    """
    db.drop_all()
    _ = client.post(
        url_for('graphql'),
        data="{ initDb }",
        content_type="application/graphql"
    )
    _ = client.post(
        url_for('graphql'),
        data="""
        {
            createPost
            (
                text: "my text",
                author: "my author",
                createdAt: "2006-01-02T15:04:05"
            )
        }
        """,
        content_type="application/graphql"
    )
    response = client.post(
        url_for('graphql'),
        data="""
        {
            deletePost(postId: 1)
        }
        """,
        content_type="application/graphql"
    )
    assert response.status_code == 200
    content = json.loads(response.text)
    assert content["data"]["deletePost"] == "ok"
