import time
from unittest.mock import MagicMock, patch

import pytest
import requests

from konnektr_graph.auth.client_secret_credential import ClientSecretCredential
from konnektr_graph.auth.device_code_credential import DeviceCodeCredential
from konnektr_graph.auth.static_token_credential import StaticTokenCredential


class TestStaticTokenCredential:
    def test_get_token(self):
        cred = StaticTokenCredential("my-token")
        assert cred.get_token() == "my-token"

    def test_get_headers(self):
        cred = StaticTokenCredential("my-token")
        assert cred.get_headers() == {"Authorization": "Bearer my-token"}

    def test_expired_token(self):
        cred = StaticTokenCredential("expired", expires_on=time.time() - 10)
        with pytest.raises(Exception, match="Token has expired"):
            cred.get_token()

    def test_is_expired(self):
        cred = StaticTokenCredential("t", expires_on=time.time() - 1)
        assert cred.is_expired is True

    def test_not_expired(self):
        cred = StaticTokenCredential("t", expires_on=time.time() + 3600)
        assert cred.is_expired is False

    def test_no_expiry(self):
        cred = StaticTokenCredential("t")
        assert cred.is_expired is False


class TestClientSecretCredential:
    def test_get_token_caches(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "cached-token",
            "expires_in": 3600,
        }
        cred = ClientSecretCredential(
            domain="auth.example.com",
            audience="api://default",
            client_id="cid",
            client_secret="secret",
        )
        with patch.object(requests, "post", return_value=mock_response) as mock_post:
            token1 = cred.get_token()
            token2 = cred.get_token()
            assert token1 == "cached-token"
            assert token2 == "cached-token"
            assert mock_post.call_count == 1

    def test_get_headers(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "header-token",
            "expires_in": 3600,
        }
        cred = ClientSecretCredential(
            domain="auth.example.com",
            audience="api://default",
            client_id="cid",
            client_secret="secret",
        )
        with patch.object(requests, "post", return_value=mock_response):
            headers = cred.get_headers()
            assert headers == {"Authorization": "Bearer header-token"}


class TestDeviceCodeCredential:
    def test_get_token_success(self):
        cred = DeviceCodeCredential(
            domain="auth.example.com",
            audience="api://default",
            client_id="cid",
            prompt_callback=lambda u, uc, c: None,
        )
        mock_device_response = MagicMock()
        mock_device_response.json.return_value = {
            "device_code": "dev123",
            "user_code": "ABC-123",
            "verification_uri": "https://auth.example.com/activate",
            "verification_uri_complete": "https://auth.example.com/activate?code=ABC-123",
            "interval": 1,
            "expires_in": 900,
        }
        mock_token_response = MagicMock()
        mock_token_response.json.return_value = {
            "access_token": "device-token",
            "expires_in": 3600,
        }
        with patch.object(
            requests, "post", side_effect=[mock_device_response, mock_token_response]
        ) as mock_post:
            token = cred.get_token()
            assert token == "device-token"
            assert mock_post.call_count == 2

    def test_get_token_authorization_pending(self):
        cred = DeviceCodeCredential(
            domain="auth.example.com",
            audience="api://default",
            client_id="cid",
            prompt_callback=lambda u, uc, c: None,
        )
        mock_device_response = MagicMock()
        mock_device_response.json.return_value = {
            "device_code": "dev123",
            "user_code": "ABC-123",
            "verification_uri": "https://auth.example.com/activate",
            "verification_uri_complete": "https://auth.example.com/activate?code=ABC-123",
            "interval": 1,
            "expires_in": 900,
        }
        mock_pending_response = MagicMock()
        mock_pending_response.json.return_value = {"error": "authorization_pending"}
        mock_token_response = MagicMock()
        mock_token_response.json.return_value = {
            "access_token": "pending-token",
            "expires_in": 3600,
        }
        with patch.object(
            requests,
            "post",
            side_effect=[mock_device_response, mock_pending_response, mock_token_response],
        ) as mock_post:
            token = cred.get_token()
            assert token == "pending-token"
            assert mock_post.call_count == 3

    def test_get_token_cached(self):
        cred = DeviceCodeCredential(
            domain="auth.example.com",
            audience="api://default",
            client_id="cid",
            prompt_callback=lambda u, uc, c: None,
        )
        cred._token = "cached-device-token"
        cred._expires_on = time.time() + 3600
        token = cred.get_token()
        assert token == "cached-device-token"

    def test_get_headers(self):
        cred = DeviceCodeCredential(
            domain="auth.example.com",
            audience="api://default",
            client_id="cid",
            prompt_callback=lambda u, uc, c: None,
        )
        cred._token = "header-device-token"
        cred._expires_on = time.time() + 3600
        assert cred.get_headers() == {"Authorization": "Bearer header-device-token"}
