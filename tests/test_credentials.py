from explorer.credentials import CredentialsManager
import pytest
from moto import mock_secretsmanager
import boto3


@pytest.fixture
def create_mocked_secret_manager_connection():
    with mock_secretsmanager():
        yield boto3.session.Session().client(
            service_name="secretsmanager", region_name="us-east-1"
        )


@pytest.fixture
def create_test_secret(create_mocked_secret_manager_connection):
    create_mocked_secret_manager_connection.create_secret(
        Name="mock_secret", SecretString="""{"mock_secret_key": "mock_secret_value"}""",
    )


def test_retrieve_secret_string(
    monkeypatch, create_mocked_secret_manager_connection, create_test_secret
):
    def get_mocked_secret_manager(*args, **kwargs):
        return create_mocked_secret_manager_connection

    monkeypatch.setattr(
        CredentialsManager, "_create_boto_client", get_mocked_secret_manager,
    )

    credentials_client = CredentialsManager("mock_secret")

    assert credentials_client.retrieve_secret_string() == {
        "mock_secret_key": "mock_secret_value"
    }


def test_unexisting_secret():
    credentials_client = CredentialsManager("secret_that_doesnt_exist")

    with pytest.raises(Exception) as excinfo:
        credentials_client.retrieve_secret_string()

    assert "ResourceNotFoundException" in str(excinfo.errisinstance)
    assert "Secrets Manager can't find the specified secret" in str(excinfo.value)


def test_wrong_region():
    with pytest.raises(Exception) as excinfo:
        CredentialsManager(
            "some_secret", "region_that_doesnt_exist"
        ).retrieve_secret_string()

    assert (
        "Invalid endpoint: https://secretsmanager.region_that_doesnt_exist.amazonaws.com"
        in str(excinfo.value)
    )
