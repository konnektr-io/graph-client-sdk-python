# konnektr_graph/auth/async_azure_identity_credential_adapter.py
"""
Async adapter for using Azure SDK credentials (e.g., DefaultAzureCredential)
with Konnektr Graph's AsyncTokenProvider protocol.
"""
from typing import Dict, Optional


class AsyncAzureIdentityCredentialAdapter:
    """
    Adapts an Azure SDK AsyncTokenCredential to Konnektr Graph's AsyncTokenProvider.

    Works with async credentials from ``azure-identity.aio`` such as
    ``DefaultAzureCredential`` and ``ManagedIdentityCredential``.

    :param credential: Azure async credential object implementing ``get_token(scope)``.
    :param scope: OAuth scope to request. For ADT-compatible APIs, use
        ``https://digitaltwins.azure.net/.default``.
    """

    def __init__(self, credential: object, *, scope: str):
        if not scope:
            raise ValueError("scope is required")
        self.credential = credential
        self.scope = scope

    async def get_token(self) -> str:
        token = await self.credential.get_token(self.scope)  # type: ignore[attr-defined]
        return token.token

    async def get_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {await self.get_token()}"}


class AsyncDefaultAzureCredentialAdapter(AsyncAzureIdentityCredentialAdapter):
    """
    Backward-compatible alias for AsyncAzureIdentityCredentialAdapter.

    This class name is intentionally specific to highlight the common use case
    with ``azure.identity.aio.DefaultAzureCredential``.
    """

    def __init__(self, credential: object, *, scope: Optional[str] = None):
        super().__init__(
            credential,
            scope=scope or "https://digitaltwins.azure.net/.default",
        )
