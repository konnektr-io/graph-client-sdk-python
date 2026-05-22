# konnektr_graph/auth/azure_identity_credential_adapter.py
"""
Adapter for using Azure SDK credentials (e.g., DefaultAzureCredential)
with Konnektr Graph's TokenProvider protocol.
"""
from typing import Dict, Optional


class AzureIdentityCredentialAdapter:
    """
    Adapts an Azure SDK TokenCredential to Konnektr Graph's TokenProvider.

    Works with credentials from ``azure-identity`` such as
    ``DefaultAzureCredential``, ``ClientSecretCredential``,
    and ``ManagedIdentityCredential``.

    :param credential: Azure credential object implementing ``get_token(scope)``.
    :param scope: OAuth scope to request. For ADT-compatible APIs, use
        ``https://digitaltwins.azure.net/.default``.
    """

    def __init__(self, credential: object, *, scope: str):
        if not scope:
            raise ValueError("scope is required")
        self.credential = credential
        self.scope = scope

    def get_token(self) -> str:
        token = self.credential.get_token(self.scope)  # type: ignore[attr-defined]
        return token.token

    def get_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.get_token()}"}


class DefaultAzureCredentialAdapter(AzureIdentityCredentialAdapter):
    """
    Backward-compatible alias for AzureIdentityCredentialAdapter.

    This class name is intentionally specific to highlight the common use case
    with ``azure.identity.DefaultAzureCredential``.
    """

    def __init__(self, credential: object, *, scope: Optional[str] = None):
        super().__init__(
            credential,
            scope=scope or "https://digitaltwins.azure.net/.default",
        )
