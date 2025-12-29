# Example usage of the KonnektrGraphClient with KonnektrCredential
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
    twin_id = "myTwinId"
    try:
        twin = client.get_digital_twin(twin_id)
        print("Digital Twin:", twin)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
