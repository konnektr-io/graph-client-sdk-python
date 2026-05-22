"""Example: Use Async DefaultAzureCredential with Konnektr Graph SDK."""

import asyncio

from azure.identity.aio import DefaultAzureCredential

from konnektr_graph.aio import KonnektrGraphClient
from konnektr_graph.auth import AsyncDefaultAzureCredentialAdapter


async def main() -> None:
    endpoint = "https://your-konnektr-api-endpoint"

    # Uses environment/service principal/managed identity/CLI in standard Azure order.
    azure_cred = DefaultAzureCredential()

    # For ADT-compatible APIs use this scope (audience + '/.default').
    cred = AsyncDefaultAzureCredentialAdapter(
        azure_cred,
        scope="https://digitaltwins.azure.net/.default",
    )

    async with KonnektrGraphClient(endpoint, cred) as client:
        twin = await client.get_digital_twin("myTwinId")
        print(twin)

    await azure_cred.close()


if __name__ == "__main__":
    asyncio.run(main())
