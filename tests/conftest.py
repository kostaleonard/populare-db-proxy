"""Contains test fixtures."""

import os
import pytest
import boto3
from moto import mock_rds

TEST_REGION = "us-east-2"
DB_NAME = "populare_db"
DB_INSTANCE_IDENTIFIER = "populare-db-instance"
ALLOCATED_STORAGE_GB = 5
DB_INSTANCE_CLASS = "db.t2.micro"
MASTER_USERNAME = "testing"
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
def fixture_mocked_rds(aws_credentials: None) -> None:
    """Creates a mocked RDS instance for tests.

    :param aws_credentials: Mocked AWS credentials.
    """
    # pylint: disable=unused-argument
    with mock_rds():
        client = boto3.client("rds", region_name=TEST_REGION)
        client.create_db_instance(
            DBName=DB_NAME,
            DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER,
            AllocatedStorage=ALLOCATED_STORAGE_GB,
            DBInstanceClass=DB_INSTANCE_CLASS,
            Engine="mysql",
            MasterUsername=MASTER_USERNAME,
            MasterUserPassword="testingtesting",
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
        yield
