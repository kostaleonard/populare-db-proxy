"""Tests app_data.py."""

import os
import pytest
from unittest.mock import patch
from populare_db_proxy.app_data import app, get_database_uri

TEST_SECRET_FILENAME = "/tmp/populare-db-proxy/test_app_data/db-certs/db-uri"


def test_database_uri_is_set() -> None:
    """Tests that the Flask-SQLAlchemy database URI is set."""
    assert app.config["SQLALCHEMY_DATABASE_URI"]


@patch.dict('os.environ')
def test_get_database_uri_raises_error_missing_secret() -> None:
    """Tests that get_database_uri raises an error if the secret is missing."""
    # POPULARE_ALLOW_MISSING_SECRET is set in conftest for local tests.
    del os.environ["POPULARE_ALLOW_MISSING_SECRET"]
    with pytest.raises(FileNotFoundError):
        _ = get_database_uri()


def test_get_database_uri_reads_secret() -> None:
    """Tests that get_database_uri reads the secret file."""
    test_uri = "xxxxxxxxxxxxxxx.xxxxxxxxxxxx.us-east-1.rds.amazonaws.com"
    os.makedirs(os.path.dirname(TEST_SECRET_FILENAME), exist_ok=True)
    with open(TEST_SECRET_FILENAME, "w", encoding="utf-8") as outfile:
        outfile.write(test_uri)
    db_uri = get_database_uri(TEST_SECRET_FILENAME)
    assert db_uri == test_uri
