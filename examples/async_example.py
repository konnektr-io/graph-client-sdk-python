# examples/async_example.py
import asyncio
from konnektr_graph.aio import KonnektrGraphClient
from konnektr_graph.auth import AsyncClientSecretCredential

async def main():
    endpoint = "https://your-konnektr-api-endpoint"
    
    cred = AsyncClientSecretCredential(
        domain="auth.konnektr.io",
        audience="https://graph.konnektr.io",
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET"
    )
    
    async with KonnektrGraphClient(endpoint, cred) as client:
        try:
            # Query twins
            print("Querying twins asynchronously...")
            async for twin in client.query_twins("SELECT * FROM digitaltwins"):
                print(f"Twin ID: {twin.get('$dtId')}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
