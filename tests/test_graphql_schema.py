"""Tests graphql_schema.py.

Tests the GraphQL schema directly, without using Flask; test_proxy.py contains
tests that issue POST requests on the graphql endpoint directly.
"""

from populare_db_proxy.app_data import db
from populare_db_proxy.graphql_schema import get_schema


def test_resolve_init_returns_ok() -> None:
    """Tests that resolve_init_db returns ok."""
    db.drop_all()
    schema = get_schema()
    result = schema.execute("""
    {
        initDb
    }
    """)
    assert result.data["initDb"] == "ok"
