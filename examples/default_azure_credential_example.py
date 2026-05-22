"""Example: Use DefaultAzureCredential with Konnektr Graph SDK."""

from azure.identity import DefaultAzureCredential

from konnektr_graph import KonnektrGraphClient
from konnektr_graph.auth import DefaultAzureCredentialAdapter


def main() -> None:
    endpoint = "https://your-konnektr-api-endpoint"

    # Uses environment/service principal/managed identity/CLI in standard Azure order.
    azure_cred = DefaultAzureCredential()

    # For ADT-compatible APIs use this scope (audience + '/.default').
    cred = DefaultAzureCredentialAdapter(
        azure_cred,
        scope="https://digitaltwins.azure.net/.default",
    )

    client = KonnektrGraphClient(endpoint, cred)

    twin = client.get_digital_twin("myTwinId")
    print(twin)


if __name__ == "__main__":
    main()
