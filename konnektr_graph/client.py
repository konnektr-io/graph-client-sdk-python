# konnektr_digitaltwins/client.py
"""
Konnektr Graph SDK (Azure-free)
"""
import requests
from typing import Any, Dict, Optional


# Recommend using KonnektrCredential from auth.py for authentication
from .auth import KonnektrCredential


from .models import QueryResult


class KonnektrGraphClient:
    def __init__(self, endpoint: str, auth):
        """
        :param endpoint: API endpoint (e.g. https://graph.konnektr.io)
        :param auth: An object with a get_headers() method (e.g. KonnektrCredential)
        """
        if not endpoint.startswith("http"):
            endpoint = "https://" + endpoint
        self.endpoint = endpoint.rstrip("/")
        self.auth = auth

    def get_digital_twin(
        self, digital_twin_id: str, *, api_version: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Get a digital twin (Konnektr)."""
        url = f"{self.endpoint}/digitaltwins/{digital_twin_id}"
        params = {}
        if api_version:
            params["api-version"] = api_version
        headers = {"Accept": "application/json"}
        headers.update(self.auth.get_headers())
        response = requests.get(url, headers=headers, params=params, **kwargs)
        if response.status_code == 404:
            raise Exception(f"Digital twin '{digital_twin_id}' not found.")
        if not response.ok:
            raise Exception(f"Error {response.status_code}: {response.text}")
        return response.json()

    def query_twins(
        self,
        query: str,
        *,
        api_version: Optional[str] = None,
        max_items_per_page: Optional[int] = None,
        **kwargs: Any,
    ) -> QueryResult:
        """Query digital twins (Konnektr). Returns a QueryResult with .value and .next_link."""
        url = f"{self.endpoint}/query"
        params = {}
        if api_version:
            params["api-version"] = api_version
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        headers.update(self.auth.get_headers())
        body = {"query": query}
        if max_items_per_page is not None:
            headers["max-items-per-page"] = str(max_items_per_page)
        response = requests.post(
            url, headers=headers, params=params, json=body, **kwargs
        )
        if not response.ok:
            raise Exception(f"Error {response.status_code}: {response.text}")
        return QueryResult.from_dict(response.json())
