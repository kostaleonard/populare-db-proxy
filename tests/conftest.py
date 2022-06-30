"""Contains test fixtures."""
# pylint: disable=wrong-import-position

import os
TEST_DATABASE_PATH = "/tmp/populare_test.db"
os.environ["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{TEST_DATABASE_PATH}"
from datetime import datetime
import pytest
import boto3
from moto import mock_rds
from flask import Flask
from sqlalchemy.engine import Engine
from populare_db_proxy.db_schema import Post
from populare_db_proxy.db_ops import init_db_schema, create_post
from populare_db_proxy.app_data import db, app as proxy_app
from populare_db_proxy.proxy import create_app

TEST_REGION = "us-east-2"
DB_NAME = "populare_db"
DB_INSTANCE_IDENTIFIER = "populare-db-instance"
ALLOCATED_STORAGE_GB = 5
DB_INSTANCE_CLASS = "db.t2.micro"
MASTER_USERNAME = "testing"
MASTER_PASSWORD = "testingtesting"
PORT = 3306
MAX_ALLOCATED_STORAGE_GB = 20


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


@pytest.fixture(name="uninitialized_local_db")
def fixture_uninitialized_local_db() -> Engine:
    """Creates a schema-less local SQLite database for testing.

    :return: A connection to the local database.
    """
    db.drop_all()
    yield db.engine
    db.drop_all()


@pytest.fixture(name="empty_local_db")
def fixture_empty_local_db(uninitialized_local_db: Engine) -> Engine:
    """Creates an empty local SQLite database for testing.

    :return: A connection to the local database.
    """
    init_db_schema()
    yield uninitialized_local_db


@pytest.fixture(name="populated_local_db")
def fixture_populated_local_db(empty_local_db: Engine) -> Engine:
    """Creates a populated local SQLite database for testing.

    :return: A connection to the local database.
    """
    for idx in range(5):
        post = Post(
            text=f"text{idx}",
            author=f"author{idx}",
            created_at=datetime.now()
        )
        create_post(post)
    yield empty_local_db


@pytest.fixture(scope="session")
def app() -> Flask:
    """Creates the proxy flask app for testing.

    :return: The proxy flask app.
    """
    create_app(proxy_app)
    return proxy_app
