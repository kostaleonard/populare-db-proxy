"""Tests rds.py."""

from datetime import datetime
import pytest
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from populare_db_proxy.db_schema import Post
from populare_db_proxy.rds import init_db_schema, create_post
from tests.conftest import DB_NAME


def test_rds_creation(mocked_rds: dict) -> None:
    """Tests that the mocked RDS was created successfully.

    :param mocked_rds: The mocked database JSON object.
    """
    assert mocked_rds["DBInstance"]["DBName"] == DB_NAME


def test_local_db_creation(populated_local_db: Engine) -> None:
    """Tests that the local database was created successfully.

    :param populated_local_db: A connection to the local, in-memory database.
    """
    with Session(populated_local_db) as session:
        with session.begin():
            statement = select(Post)
            results = session.execute(statement)
            assert list(results)


def test_init_db_schema_creates_tables(
        uninitialized_local_db: Engine
) -> None:
    """Tests that init_db_schema creates tables in the database.

    :param uninitialized_local_db: A connection to the local, in-memory
        database.
    """
    post = Post(text="text", author="author", created_at=datetime.now())
    with pytest.raises(OperationalError):
        # Because there are no tables, inserting raises an error.
        create_post(uninitialized_local_db, post)
    init_db_schema(uninitialized_local_db)
    create_post(uninitialized_local_db, post)
    assert post.id


def test_init_db_schema_twice_no_error(
        uninitialized_local_db: Engine
) -> None:
    """Tests that init_db_schema can be called twice without causing errors.

    :param uninitialized_local_db: A connection to the local, in-memory
        database.
    """
    post = Post(text="text", author="author", created_at=datetime.now())
    init_db_schema(uninitialized_local_db)
    init_db_schema(uninitialized_local_db)
    create_post(uninitialized_local_db, post)
    assert post.id
