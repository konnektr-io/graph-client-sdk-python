import pytest

from konnektr_graph.auth.static_token_credential import StaticTokenCredential


@pytest.fixture
def token():
    return "test-token-12345"


@pytest.fixture
def credential(token):
    return StaticTokenCredential(token)


@pytest.fixture
def endpoint():
    return "https://graph.konnektr.io"
