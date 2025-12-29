# Example usage of the KonnektrGraphClient with query_twins and KonnektrCredential
from konnektr_graph.client import KonnektrGraphClient
from konnektr_graph.auth import KonnektrCredential

def main():
    endpoint = "https://your-konnektr-api-endpoint"
    # For client credentials flow:
    cred = KonnektrCredential(
        domain="auth.konnektr.io",
        audience="https://graph.konnektr.io",
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET"
    )
    # For device code flow, use:
    # cred = KonnektrCredential(
    #     domain="auth.konnektr.io",
    #     audience="https://graph.konnektr.io",
    #     client_id="YOUR_DEVICE_CODE_CLIENT_ID",
    #     use_device_code=True
    # )
    client = KonnektrGraphClient(endpoint, cred)
    query = "SELECT * FROM digitaltwins"
    try:
        result = client.query_twins(query)
        print("Query returned", len(result.value), "items.")
        for twin in result.value:
            print(twin)
        if result.next_link:
            print("Next page link:", result.next_link)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
