"""Tests proxy.py.

This test file contains all Flask tests; other components, e.g., the GraphQL
schema, are tested in isolation of Flask.
"""

import json
from flask import url_for
from flask.testing import FlaskClient
from populare_db_proxy.app_data import db


def test_get_graphql_endpoint_gives_bad_response(client: FlaskClient) -> None:
    """Tests that a GET request on the graphql endpoint gives code 400.

    :param client: The flask client.
    """
    assert client.get(url_for('graphql')).status_code == 400


def test_post_graphql_endpoint_gives_ok_response(client: FlaskClient) -> None:
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


# TODO add tests for update and delete POST requests
