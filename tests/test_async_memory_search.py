from unittest.mock import AsyncMock, MagicMock

import pytest

from konnektr_graph.aio.client import KonnektrGraphClient
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


@pytest.fixture
def async_credential():
    cred = MagicMock()
    cred.get_headers = MagicMock(return_value={"Authorization": "Bearer async-token"})
    return cred


@pytest.fixture
def aclient(endpoint, async_credential):
    return KonnektrGraphClient(endpoint, async_credential)


SEARCH_RESULT_WIRE = {
    "id": "memory-42",
    "modelId": "dtmi:example:MemoryRecord;1",
    "distance": 0.013,
    "excerpt": '{"scopeKey":"workspace-a"}',
    "lastUpdatedOn": "2026-09-18T08:12:44+00:00",
}


class TestAsyncSearchMemorySerialization:
    @pytest.mark.asyncio
    async def test_full_body_uses_camel_case(self, aclient):
        captured = {}

        async def fake_request(method, url, **kwargs):
            captured["method"] = method
            captured["url"] = url
            captured["json"] = kwargs.get("json")
            return [SEARCH_RESULT_WIRE]

        aclient._request = fake_request  # type: ignore[method-assign]
        results = await aclient.search_memory(
            vector=[0.11, -0.02, 0.58],
            embedding_property="embedding",
            limit=5,
            model_ids=["dtmi:example:MemoryRecord;1"],
            property_filters={"environmentId": "env-1", "userId": "user-9"},
            related_twin_id="session-9",
            expected_dimension=3,
            excerpt_length=500,
        )
        assert captured["method"] == "POST"
        assert captured["url"] == f"{aclient.endpoint}/digitaltwins/memory-search"
        assert captured["json"] == {
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
        assert results[0].id == "memory-42"
        assert results[0].model_id == "dtmi:example:MemoryRecord;1"

    @pytest.mark.asyncio
    async def test_minimal_body_shape(self, aclient):
        captured = {}

        async def fake_request(method, url, **kwargs):
            captured["json"] = kwargs.get("json")
            return []

        aclient._request = fake_request  # type: ignore[method-assign]
        results = await aclient.search_memory(vector=[0.5, 0.5])
        assert captured["json"] == {
            "vector": [0.5, 0.5],
            "embeddingProperty": "embedding",
            "limit": 10,
        }
        assert results == []

    @pytest.mark.asyncio
    async def test_results_omit_null_model_and_timestamp(self, aclient):
        async def fake_request(method, url, **kwargs):
            return [{"id": "m-1", "distance": 0.5, "excerpt": "{}"}]

        aclient._request = fake_request  # type: ignore[method-assign]
        (record,) = await aclient.search_memory(vector=[0.1])
        assert record.model_id is None
        assert record.last_updated_on is None


class TestAsyncSearchMemoryClientValidation:
    @pytest.mark.parametrize(
        "kwargs",
        [
            {"vector": []},
            {"vector": [0.1, float("nan")]},
            {"vector": [0.1], "limit": 0},
            {"vector": [0.1], "limit": 101},
            {"vector": [0.1], "embedding_property": "not a property!"},
            {"vector": [0.1], "property_filters": {"bad key!": "v"}},
            {"vector": [0.1, 0.2], "expected_dimension": 3},
            {"vector": [0.1], "excerpt_length": 4001},
        ],
    )
    @pytest.mark.asyncio
    async def test_invalid_options_raise_without_http_call(self, aclient, kwargs):
        aclient._request = AsyncMock()  # type: ignore[method-assign]
        with pytest.raises(ValidationError):
            await aclient.search_memory(**kwargs)
        aclient._request.assert_not_called()  # type: ignore[attr-defined]


class TestAsyncSearchMemoryServerErrors:
    @pytest.mark.asyncio
    async def test_400_maps_to_validation_error(self, aclient):
        mock_resp = MagicMock()
        mock_resp.ok = False
        mock_resp.status = 400
        mock_resp.json = AsyncMock(
            return_value={"errors": {"vector": ["Query vector is required."]}}
        )
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        with pytest.raises(ValidationError) as exc_info:
            await aclient.search_memory(vector=[0.1])
        assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_503_maps_to_service_unavailable(self, aclient):
        mock_resp = MagicMock()
        mock_resp.ok = False
        mock_resp.status = 503
        mock_resp.json = AsyncMock(return_value={"detail": "pgvector missing"})
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        with pytest.raises(ServiceUnavailableError) as exc_info:
            await aclient.search_memory(vector=[0.1])
        assert exc_info.value.status_code == 503

    @pytest.mark.asyncio
    async def test_401_maps_to_authentication_error(self, aclient):
        mock_resp = MagicMock()
        mock_resp.ok = False
        mock_resp.status = 401
        mock_resp.json = AsyncMock(return_value={})
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        with pytest.raises(AuthenticationError):
            await aclient.search_memory(vector=[0.1])

    @pytest.mark.asyncio
    async def test_transport_error_maps_to_http_response_error(
        self, aclient
    ):
        import aiohttp

        mock_session = MagicMock()
        mock_session.request.side_effect = aiohttp.ClientConnectionError("down")
        aclient._session = mock_session
        with pytest.raises(HttpResponseError):
            await aclient.search_memory(vector=[0.1])


class TestAsyncEnsureMemorySearchIndex:
    @pytest.mark.asyncio
    async def test_body_and_typed_result(self, aclient):
        captured = {}

        async def fake_request(method, url, **kwargs):
            captured["method"] = method
            captured["url"] = url
            captured["json"] = kwargs.get("json")
            return {"indexName": "twin_embedding_hnsw_idx", "dimension": 3}

        aclient._request = fake_request  # type: ignore[method-assign]
        index = await aclient.ensure_memory_search_index(
            dimension=3, m=16, ef_construction=64
        )
        assert captured["method"] == "POST"
        assert captured["url"] == f"{aclient.endpoint}/digitaltwins/memory-search/index"
        assert captured["json"] == {
            "embeddingProperty": "embedding",
            "dimension": 3,
            "m": 16,
            "efConstruction": 64,
        }
        assert isinstance(index, MemorySearchIndex)
        assert index.index_name == "twin_embedding_hnsw_idx"
        assert index.dimension == 3

    @pytest.mark.asyncio
    async def test_invalid_options_raise_without_http_call(self, aclient):
        aclient._request = AsyncMock()  # type: ignore[method-assign]
        with pytest.raises(ValidationError):
            await aclient.ensure_memory_search_index(dimension=0)
        aclient._request.assert_not_called()  # type: ignore[attr-defined]


class TestAsyncGetMemorySearchCapability:
    @pytest.mark.asyncio
    async def test_get_url_and_typed_result(self, aclient):
        captured = {}

        async def fake_request(method, url, **kwargs):
            captured["method"] = method
            captured["url"] = url
            return {"vectorSearchAvailable": True}

        aclient._request = fake_request  # type: ignore[method-assign]
        capability = await aclient.get_memory_search_capability()
        assert captured["method"] == "GET"
        assert (
            captured["url"]
            == f"{aclient.endpoint}/digitaltwins/memory-search/capability"
        )
        assert isinstance(capability, MemorySearchCapability)
        assert capability.vector_search_available is True
