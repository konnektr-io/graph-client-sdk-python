"""
Konnektr Graph Auth - Unified Credential for client credentials and device code
"""

import requests
import time
import webbrowser


class KonnektrCredential:
    def __init__(
        self,
        domain: str,
        audience: str,
        client_id: str,
        client_secret: str | None = None,
        use_device_code: bool = False,
        scope: str = "openid profile email",
    ):
        self.domain = domain
        self.audience = audience
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.use_device_code = use_device_code
        self._token = None
        self._expires_on = 0

    def get_token(self):
        if self._token and time.time() < self._expires_on - 300:
            return self._token
        if self.use_device_code:
            return self._get_token_device_code()
        else:
            return self._get_token_client_credentials()

    def _get_token_client_credentials(self):
        url = f"https://{self.domain}/oauth/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
            "grant_type": "client_credentials",
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        token_data = response.json()
        self._expires_on = time.time() + token_data["expires_in"]
        self._token = token_data["access_token"]
        return self._token

    def _get_token_device_code(self):
        device_url = f"https://{self.domain}/oauth/device/code"
        device_data = {
            "client_id": self.client_id,
            "scope": self.scope,
            "audience": self.audience,
        }
        device_response = requests.post(device_url, json=device_data)
        device_info = device_response.json()
        print(f"Please visit: {device_info['verification_uri_complete']}")
        print(
            f"Or go to {device_info['verification_uri']} and enter: {device_info['user_code']}"
        )
        webbrowser.open(device_info["verification_uri_complete"])

        token_url = f"https://{self.domain}/oauth/token"
        token_data = {
            "client_id": self.client_id,
            "device_code": device_info["device_code"],
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }
        interval = device_info.get("interval", 5)
        while True:
            token_response = requests.post(token_url, json=token_data)
            token_result = token_response.json()
            if "error" in token_result:
                if token_result["error"] == "authorization_pending":
                    print("Waiting for authentication...")
                    time.sleep(interval)
                else:
                    raise Exception(f"Error: {token_result['error']}")
            else:
                self._expires_on = time.time() + token_result["expires_in"]
                self._token = token_result["access_token"]
                print("Authentication successful!")
                return self._token

    def get_headers(self):
        return {"Authorization": f"Bearer {self.get_token()}"}
