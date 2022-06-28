"""Tests app_data.py."""

from populare_db_proxy.app_data import app


def test_database_uri_is_set() -> None:
    """Tests that the Flask-SQLAlchemy database URI is set."""
    assert app.config["SQLALCHEMY_DATABASE_URI"]
