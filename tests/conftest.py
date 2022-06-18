"""Contains test fixtures."""

import os
import pytest
import boto3
from moto import mock_rds
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy.engine import Connection

TEST_REGION = "us-east-2"
DB_NAME = "populare_db"
DB_INSTANCE_IDENTIFIER = "populare-db-instance"
ALLOCATED_STORAGE_GB = 5
DB_INSTANCE_CLASS = "db.t2.micro"
MASTER_USERNAME = "testing"
MASTER_PASSWORD = "testingtesting"
PORT = 3306
MAX_ALLOCATED_STORAGE_GB = 20
TEST_IN_MEM_DB_URL = "sqlite+pysqlite:///:memory:"


@pytest.fixture(name="aws_credentials", scope="session")
def fixture_aws_credentials() -> None:
    """Mocked AWS credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = TEST_REGION


@pytest.fixture(name="mocked_rds", scope="session")
def fixture_mocked_rds(aws_credentials: None) -> dict:
    """Creates a mocked RDS instance for tests.

    :param aws_credentials: Mocked AWS credentials.
    :return: The mocked database JSON object.
    """
    # pylint: disable=unused-argument
    with mock_rds():
        client = boto3.client("rds", region_name=TEST_REGION)
        db_instance = client.create_db_instance(
            DBName=DB_NAME,
            DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER,
            AllocatedStorage=ALLOCATED_STORAGE_GB,
            DBInstanceClass=DB_INSTANCE_CLASS,
            Engine="mysql",
            MasterUsername=MASTER_USERNAME,
            MasterUserPassword=MASTER_PASSWORD,
            BackupRetentionPeriod=1,
            Port=PORT,
            MultiAZ=False,
            EngineVersion="8.0",
            PubliclyAccessible=False,
            Tags=[
                {
                    "Key": "app",
                    "Value": "populare"
                }
            ],
            StorageType="standard",
            MonitoringInterval=0,
            MaxAllocatedStorage=MAX_ALLOCATED_STORAGE_GB
        )
        yield db_instance


@pytest.fixture(name="local_db")
def fixture_local_db() -> Connection:
    """Creates a local SQLite database for testing.

    :return: A connection to the local, in-memory database.
    """
    engine = create_engine(TEST_IN_MEM_DB_URL)
    with engine.connect() as conn:
        # TODO populate the database
        meta = MetaData()
        students = Table(
            'students', meta,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('lastname', String),
        )
        meta.create_all(engine)
        yield conn
