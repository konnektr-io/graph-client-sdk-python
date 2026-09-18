from unittest.mock import MagicMock, patch

import pytest
import requests

from konnektr_graph.client import KonnektrGraphClient
from konnektr_graph.exceptions import (
    AuthenticationError,
    HttpResponseError,
    ServiceUnavailableError,
    ValidationError,
)
from konnektr_graph.models import (
    MemorySearchCapability,
    MemorySearchIndex,
    MemorySearchResult,
)


def make_mock_response(status_code=200, json_data=None, headers=None):
    mock = MagicMock(spec=requests.Response)
    mock.status_code = status_code
    mock.ok = 200 <= status_code < 300
    mock.json.return_value = json_data if json_data is not None else {}
    mock.headers = headers or {}
    return mock


SEARCH_RESULT_WIRE = {
    "id": "memory-42",
    "modelId": "dtmi:example:MemoryRecord;1",
    "distance": 0.013,
    "excerpt": '{"scopeKey":"workspace-a"}',
    "lastUpdatedOn": "2026-09-18T08:12:44+00:00",
}


class TestSearchMemorySerialization:
    def test_full_body_uses_camel_case(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(json_data=[SEARCH_RESULT_WIRE])
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            results = client.search_memory(
                vector=[0.11, -0.02, 0.58],
                embedding_property="embedding",
                limit=5,
                model_ids=["dtmi:example:MemoryRecord;1"],
                property_filters={"environmentId": "env-1", "userId": "user-9"},
                related_twin_id="session-9",
                expected_dimension=3,
                excerpt_length=500,
            )
            assert mock_req.call_args[0][0] == "POST"
            assert (
                mock_req.call_args[0][1]
                == f"{client.endpoint}/digitaltwins/memory-search"
            )
            body = mock_req.call_args[1]["json"]
            assert body == {
                "vector": [0.11, -0.02, 0.58],
                "embeddingProperty": "embedding",
                "limit": 5,
                "modelIds": ["dtmi:example:MemoryRecord;1"],
                "propertyFilters": {"environmentId": "env-1", "userId": "user-9"},
                "relatedTwinId": "session-9",
                "expectedDimension": 3,
                "excerptLength": 500,
            }
            assert len(results) == 1
            assert isinstance(results[0], MemorySearchResult)

    def test_minimal_body_omits_unset_optionals(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(json_data=[])
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            results = client.search_memory(vector=[0.5, 0.5])
            body = mock_req.call_args[1]["json"]
            assert body == {
                "vector": [0.5, 0.5],
                "embeddingProperty": "embedding",
                "limit": 10,
            }
            assert results == []

    def test_results_deserialize_typed(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(json_data=[SEARCH_RESULT_WIRE])
        with patch.object(requests, "request", return_value=mock_resp):
            (record,) = client.search_memory(vector=[0.1, 0.2])
            assert record.id == "memory-42"
            assert record.model_id == "dtmi:example:MemoryRecord;1"
            assert record.distance == pytest.approx(0.013)
            assert record.excerpt == '{"scopeKey":"workspace-a"}'
            assert record.last_updated_on == "2026-09-18T08:12:44+00:00"

    def test_results_omit_null_model_and_timestamp(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(
            json_data=[{"id": "m-1", "distance": 0.5, "excerpt": "{}"}]
        )
        with patch.object(requests, "request", return_value=mock_resp):
            (record,) = client.search_memory(vector=[0.1])
            assert record.model_id is None
            assert record.last_updated_on is None

    def test_credential_headers_and_api_version_forwarded(
        self, credential, endpoint
    ):
        client = KonnektrGraphClient(
            endpoint, credential, api_version="2025-01-01"
        )
        mock_resp = make_mock_response(json_data=[])
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.search_memory(vector=[0.1])
            headers = mock_req.call_args[1]["headers"]
            assert headers["Authorization"] == "Bearer test-token-12345"
            assert headers["Content-Type"] == "application/json"
            assert mock_req.call_args[1]["params"] == {
                "api-version": "2025-01-01"
            }


class TestSearchMemoryClientValidation:
    @pytest.mark.parametrize(
        "kwargs",
        [
            {"vector": []},
            {"vector": [0.1, float("nan")]},
            {"vector": [0.1, float("inf")]},
            {"vector": [0.1], "limit": 0},
            {"vector": [0.1], "limit": 101},
            {"vector": [0.1], "embedding_property": "not a property!"},
            {"vector": [0.1], "model_ids": [""]},
            {"vector": [0.1], "property_filters": {"bad key!": "v"}},
            {"vector": [0.1], "property_filters": {"ok": None}},
            {"vector": [0.1], "related_twin_id": "  "},
            {"vector": [0.1, 0.2], "expected_dimension": 3},
            {"vector": [0.1], "excerpt_length": 0},
            {"vector": [0.1], "excerpt_length": 4001},
        ],
    )
    def test_invalid_options_raise_without_http_call(
        self, credential, endpoint, kwargs
    ):
        client = KonnektrGraphClient(endpoint, credential)
        with patch.object(requests, "request") as mock_req:
            with pytest.raises(ValidationError):
                client.search_memory(**kwargs)
            mock_req.assert_not_called()


class TestSearchMemoryServerErrors:
    def test_400_maps_to_validation_error(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(
            status_code=400,
            json_data={"errors": {"vector": ["Query vector is required."]}},
        )
        with patch.object(requests, "request", return_value=mock_resp):
            with pytest.raises(ValidationError) as exc_info:
                client.search_memory(vector=[0.1])
            assert exc_info.value.status_code == 400

    def test_503_maps_to_service_unavailable(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(
            status_code=503, json_data={"detail": "pgvector is not installed"}
        )
        with patch.object(requests, "request", return_value=mock_resp):
            with pytest.raises(ServiceUnavailableError) as exc_info:
                client.search_memory(vector=[0.1])
            assert exc_info.value.status_code == 503

    def test_401_maps_to_authentication_error(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(status_code=401, json_data={})
        with patch.object(requests, "request", return_value=mock_resp):
            with pytest.raises(AuthenticationError):
                client.search_memory(vector=[0.1])

    def test_transport_error_maps_to_http_response_error(
        self, credential, endpoint
    ):
        client = KonnektrGraphClient(endpoint, credential)
        with patch.object(
            requests, "request", side_effect=requests.ConnectionError("down")
        ):
            with pytest.raises(HttpResponseError):
                client.search_memory(vector=[0.1])


class TestEnsureMemorySearchIndex:
    def test_body_and_typed_result(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(
            json_data={"indexName": "twin_embedding_hnsw_idx", "dimension": 3}
        )
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            index = client.ensure_memory_search_index(
                dimension=3, m=16, ef_construction=64
            )
            assert mock_req.call_args[0][0] == "POST"
            assert (
                mock_req.call_args[0][1]
                == f"{client.endpoint}/digitaltwins/memory-search/index"
            )
            assert mock_req.call_args[1]["json"] == {
                "embeddingProperty": "embedding",
                "dimension": 3,
                "m": 16,
                "efConstruction": 64,
            }
            assert isinstance(index, MemorySearchIndex)
            assert index.index_name == "twin_embedding_hnsw_idx"
            assert index.dimension == 3

    def test_minimal_body_omits_tuning(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(
            json_data={"indexName": "twin_embedding_hnsw_idx", "dimension": 3}
        )
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.ensure_memory_search_index(dimension=3)
            assert mock_req.call_args[1]["json"] == {
                "embeddingProperty": "embedding",
                "dimension": 3,
            }

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"dimension": 0},
            {"dimension": 2001},
            {"dimension": 3, "embedding_property": "bad prop!"},
            {"dimension": 3, "m": 1},
            {"dimension": 3, "m": 101},
            {"dimension": 3, "ef_construction": 3},
            {"dimension": 3, "ef_construction": 1001},
        ],
    )
    def test_invalid_options_raise_without_http_call(
        self, credential, endpoint, kwargs
    ):
        client = KonnektrGraphClient(endpoint, credential)
        with patch.object(requests, "request") as mock_req:
            with pytest.raises(ValidationError):
                client.ensure_memory_search_index(**kwargs)
            mock_req.assert_not_called()

    def test_503_maps_to_service_unavailable(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(status_code=503, json_data={})
        with patch.object(requests, "request", return_value=mock_resp):
            with pytest.raises(ServiceUnavailableError):
                client.ensure_memory_search_index(dimension=3)


class TestGetMemorySearchCapability:
    def test_get_url_and_typed_result(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(
            json_data={"vectorSearchAvailable": True}
        )
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            capability = client.get_memory_search_capability()
            assert mock_req.call_args[0][0] == "GET"
            assert (
                mock_req.call_args[0][1]
                == f"{client.endpoint}/digitaltwins/memory-search/capability"
            )
            assert isinstance(capability, MemorySearchCapability)
            assert capability.vector_search_available is True

    def test_capability_unavailable(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(
            json_data={"vectorSearchAvailable": False}
        )
        with patch.object(requests, "request", return_value=mock_resp):
            capability = client.get_memory_search_capability()
            assert capability.vector_search_available is False


class TestMemorySearchModelRoundTrip:
    def test_result_round_trip_omits_nulls(self):
        record = MemorySearchResult.from_dict(SEARCH_RESULT_WIRE)
        assert record.to_dict() == SEARCH_RESULT_WIRE
        minimal = MemorySearchResult(id="m-1", distance=0.5, excerpt="{}")
        assert minimal.to_dict() == {
            "id": "m-1",
            "distance": 0.5,
            "excerpt": "{}",
        }

    def test_capability_and_index_round_trip(self):
        assert MemorySearchCapability.from_dict(
            {"vectorSearchAvailable": True}
        ).to_dict() == {"vectorSearchAvailable": True}
        assert MemorySearchIndex.from_dict(
            {"indexName": "idx", "dimension": 3}
        ).to_dict() == {"indexName": "idx", "dimension": 3}
