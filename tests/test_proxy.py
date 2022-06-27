"""Tests proxy.py."""

from flask import url_for
from flask.testing import FlaskClient


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
