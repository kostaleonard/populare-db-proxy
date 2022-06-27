"""Tests proxy.py."""

from flask import url_for


def test_get_graphql_endpoint_gives_bad_response(client):
    # TODO docstring, types
    assert client.get(url_for('graphql')).status_code == 400


def test_post_graphql_endpoint_gives_ok_response(client):
    # TODO docstring, types
    assert client.post(
        url_for('graphql'),
        data="{ initDb }",
        content_type="application/graphql"
    ).status_code == 200
