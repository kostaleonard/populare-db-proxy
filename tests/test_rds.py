"""Tests rds.py."""

from sqlalchemy.engine import Connection
from populare_db_proxy.db_schema import Base


def test_rds_creation(mocked_rds: dict) -> None:
    """Tests that the mocked RDS was created successfully.

    :param mocked_rds: The mocked database JSON object.
    """
    # The mocked RDS instance is created when this test is run.
    # If it was created successfully, there will be no errors in test setup.
    assert True


def test_local_db_creation(
        local_db: Connection
) -> None:
    """Tests that the local database was created successfully.

    :param local_db: A connection to the local, in-memory database.
    """
    #print(Base.metadata.tables)
    assert True
