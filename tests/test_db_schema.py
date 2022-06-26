"""Tests db_schema.py."""

from datetime import datetime
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from populare_db_proxy.rds import create_post
from populare_db_proxy.db_schema import Post


def test_post_fields_not_nullable(empty_local_db: Engine) -> None:
    """Tests that post fields are not nullable.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post = Post()
    with pytest.raises(IntegrityError):
        create_post(post)


def test_post_repr_contains_key_fields() -> None:
    """Tests that the __repr__ string contains key fields from the post."""
    post = Post(text="hello", author="world", created_at=datetime.now(), id=7)
    post_str = str(post)
    assert "hello" in post_str
    assert "world" in post_str
    assert "7" in post_str
