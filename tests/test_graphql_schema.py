"""Tests graphql_schema.py."""

import json
from flask import url_for
from flask.testing import FlaskClient


def test_resolve_init_db_responds_ok(client: FlaskClient) -> None:
    """Tests that a POST request on initDb responds ok.

    :param client: The flask client.
    """
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
    # TODO how do we make sure we start with a clean DB every test? tempfile for database?
    response = client.post(
        url_for('graphql'),
        data="{ readPosts }",
        content_type="application/graphql"
    )
    assert response.status_code == 200
    content = json.loads(response.text)
    print(content)
    assert "errors" in content
    assert "no such table" in content["errors"][0]["message"]
