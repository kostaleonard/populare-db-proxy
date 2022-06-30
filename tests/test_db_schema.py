"""Tests db_schema.py."""

from datetime import datetime
import json
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from populare_db_proxy.db_ops import create_post
from populare_db_proxy.db_schema import Post


def test_post_fields_not_nullable(empty_local_db: Engine) -> None:
    """Tests that post fields are not nullable.

    :param empty_local_db: A connection to the local database.
    """
    # pylint: disable=unused-argument
    post = Post()
    with pytest.raises(IntegrityError):
        create_post(post)


def test_post_repr_contains_all_fields() -> None:
    """Tests that the __repr__ string contains all fields from the post."""
    created_at = datetime(2022, 1, 2)
    post = Post(text="hello", author="world", created_at=created_at, id=7)
    post_str = str(post)
    assert "hello" in post_str
    assert "world" in post_str
    assert "7" in post_str
    assert "2022" in post_str


def test_post_repr_is_json_serialization() -> None:
    """Tests that the __repr__ string is a valid JSON serialization."""
    created_at = datetime(2022, 1, 2)
    post = Post(text="hello", author="world", created_at=created_at, id=7)
    post_str = str(post)
    post_json = json.loads(post_str)
    assert post_json["text"] == "hello"
    assert post_json["author"] == "world"
    assert post_json["id"] == 7
    assert "2022" in post_json["created_at"]
    deserialized_post = Post(
        text=post_json["text"],
        author=post_json["author"],
        created_at=datetime.fromisoformat(post_json["created_at"]),
        id=post_json["id"]
    )
    assert deserialized_post.text == post.text
    assert deserialized_post.created_at == post.created_at
