# Konnektr Graph SDK for Python

A powerful, Python SDK for [Konnektr Graph](https://konnektr.io), fully compatible with the Azure Digital Twins API but optimized for the Konnektr ecosystem.

## Features

- **Azure-Free**: No dependencies on Azure libraries.
- **Synchronous & Asynchronous**: High-performance clients for both threaded and async workflows.
- **Modular Auth**: Supports OAuth 2.0 Client Credentials, Device Code Flow, and Static Tokens.
- **Auto-Pagination**: Seamlessly iterate through large query results and resource lists.
- **Data Models**: Typed dataclasses for Digital Twins, Models, Relationships, and Jobs.

## Installation

```bash
pip install konnektr-graph
```

## Quick Start

### Synchronous Client

```python
from konnektr_graph import KonnektrGraphClient
from konnektr_graph.auth import ClientSecretCredential

# Authenticate
cred = ClientSecretCredential(
    domain="auth.konnektr.io",
    audience="https://graph.konnektr.io",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)

# Initialize Client
client = KonnektrGraphClient("https://your-graph-endpoint.konnektr.io", cred)

# Get a Digital Twin
twin = client.get_digital_twin("my-twin-id")
print(twin)

# Query Twins with auto-pagination (Cypher)
query = "MATCH (t:Twin) RETURN t"
for twin in client.query_twins(query):
    print(twin)

# Query with parameters (Cypher + `$name` placeholders, forwarded to the
# server's `parameters` field; only Cypher supports query parameters)
params = {"model": "dtmi:com:example:Room;1", "minTemp": 20}
query = "MATCH (t:Twin) WHERE t.`$metadata`.`$model` = $model AND temperature > $minTemp RETURN t"
for twin in client.query_twins(query, query_parameters=params):
    print(twin)
```

### Asynchronous Client

```python
import asyncio
from konnektr_graph.aio import KonnektrGraphClient
from konnektr_graph.auth import AsyncClientSecretCredential

async def main():
    cred = AsyncClientSecretCredential(
        domain="auth.konnektr.io",
        audience="https://graph.konnektr.io",
        client_id="...",
        client_secret="..."
    )

    async with KonnektrGraphClient("https://your-graph-endpoint.konnektr.io", cred) as client:
        twin = await client.get_digital_twin("my-twin-id")
        print(twin)

asyncio.run(main())
```

## Authentication Options

- `ClientSecretCredential` / `AsyncClientSecretCredential`: Ideal for server-to-server scenarios.
- `DeviceCodeCredential` / `AsyncDeviceCodeCredential`: Best for interactive CLI tools.
- `StaticTokenCredential`: Use when you already have a valid access token.
- `DefaultAzureCredentialAdapter` / `AsyncDefaultAzureCredentialAdapter`: Use Azure Identity credentials through the SDK auth protocol.

## Using Azure Identity (`DefaultAzureCredential`)

If your backend validates Azure AD tokens (e.g., ADT-compatible audience `https://digitaltwins.azure.net/`),
you can adapt `DefaultAzureCredential` to this SDK's `TokenProvider` interface.

Install Azure Identity in your app:

```bash
pip install "konnektr-graph[azure]"
```

Or install `azure-identity` directly if you prefer:

```bash
pip install azure-identity
```

### Sync

```python
from azure.identity import DefaultAzureCredential
from konnektr_graph import KonnektrGraphClient
from konnektr_graph.auth import DefaultAzureCredentialAdapter

endpoint = "https://your-graph-endpoint"

azure_cred = DefaultAzureCredential()
cred = DefaultAzureCredentialAdapter(
    azure_cred,
    scope="https://digitaltwins.azure.net/.default",
)

client = KonnektrGraphClient(endpoint, cred)
twin = client.get_digital_twin("my-twin-id")
print(twin)
```

### Async

```python
import asyncio
from azure.identity.aio import DefaultAzureCredential
from konnektr_graph.aio import KonnektrGraphClient
from konnektr_graph.auth import AsyncDefaultAzureCredentialAdapter

async def main():
    endpoint = "https://your-graph-endpoint"

    azure_cred = DefaultAzureCredential()
    cred = AsyncDefaultAzureCredentialAdapter(
        azure_cred,
        scope="https://digitaltwins.azure.net/.default",
    )

    async with KonnektrGraphClient(endpoint, cred) as client:
        twin = await client.get_digital_twin("my-twin-id")
        print(twin)

    await azure_cred.close()

asyncio.run(main())
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
