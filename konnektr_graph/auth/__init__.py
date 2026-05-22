# konnektr_graph/auth/__init__.py
"""
Authentication modules for Konnektr Graph SDK.
"""

from .protocol import TokenProvider, AsyncTokenProvider
from .client_secret_credential import ClientSecretCredential
from .device_code_credential import DeviceCodeCredential
from .static_token_credential import StaticTokenCredential
from .async_client_secret_credential import AsyncClientSecretCredential
from .async_device_code_credential import AsyncDeviceCodeCredential
from .azure_identity_credential_adapter import (
    AzureIdentityCredentialAdapter,
    DefaultAzureCredentialAdapter,
)
from .async_azure_identity_credential_adapter import (
    AsyncAzureIdentityCredentialAdapter,
    AsyncDefaultAzureCredentialAdapter,
)

__all__ = [
    "TokenProvider",
    "AsyncTokenProvider",
    "ClientSecretCredential",
    "DeviceCodeCredential",
    "StaticTokenCredential",
    "AsyncClientSecretCredential",
    "AsyncDeviceCodeCredential",
    "AzureIdentityCredentialAdapter",
    "DefaultAzureCredentialAdapter",
    "AsyncAzureIdentityCredentialAdapter",
    "AsyncDefaultAzureCredentialAdapter",
]
