"""Tests rds.py."""


def test_rds_creation(mocked_rds: dict) -> None:
    """Tests that the mocked RDS was created successfully.

    :param mocked_rds: The mocked database JSON object.
    """
    # The mocked RDS instance is created when this test is run.
    # If it was created successfully, there will be no errors in test setup.
    assert True
