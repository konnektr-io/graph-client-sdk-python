# Example usage of the KonnektrGraphClient with query_twins
from konnektr_graph import KonnektrGraphClient
from konnektr_graph.auth import ClientSecretCredential

def main():
    endpoint = "https://your-konnektr-api-endpoint"

    # For client credentials flow:
    cred = ClientSecretCredential(
        domain="auth.konnektr.io",
        audience="https://graph.konnektr.io",
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
    )

    client = KonnektrGraphClient(endpoint, cred)
    query = "SELECT * FROM digitaltwins"
    try:
        # Returns an iterator that handles pagination automatically
        result_iterator = client.query_twins(query)

        print("Query Results:")
        count = 0
        for twin in result_iterator:
            print(twin)
            count += 1
        print(f"Total items: {count}")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
