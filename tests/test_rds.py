"""Tests rds.py."""

from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from populare_db_proxy.db_schema import Post


def test_rds_creation(mocked_rds: dict) -> None:
    """Tests that the mocked RDS was created successfully.

    :param mocked_rds: The mocked database JSON object.
    """
    # The mocked RDS instance is created when this test is run.
    # If it was created successfully, there will be no errors in test setup.
    assert True


def test_local_db_creation(populated_local_db: Engine) -> None:
    """Tests that the local database was created successfully.

    :param populated_local_db: A connection to the local, in-memory database.
    """
    with Session(populated_local_db) as session:
        with session.begin():
            statement = select(Post)
            results = session.execute(statement)
            assert list(results)
