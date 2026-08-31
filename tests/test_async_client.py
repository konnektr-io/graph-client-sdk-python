from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from konnektr_graph.aio.client import AsyncPagedIterator, KonnektrGraphClient
from konnektr_graph.exceptions import (
    AuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
)
from konnektr_graph.models import ImportJob
from konnektr_graph.types import (
    BasicDigitalTwin,
    BasicRelationship,
    DigitalTwinMetadata,
)


@pytest.fixture
def async_credential():
    cred = MagicMock()
    cred.get_headers = MagicMock(return_value={"Authorization": "Bearer async-token"})
    return cred


@pytest.fixture
def aclient(endpoint, async_credential):
    return KonnektrGraphClient(endpoint, async_credential)


class TestAsyncClientInit:
    def test_endpoint_normalized(self, async_credential):
        client = KonnektrGraphClient("graph.konnektr.io", async_credential)
        assert client.endpoint == "https://graph.konnektr.io"

    def test_session_lifecycle(self, aclient):
        assert aclient._session is None


class TestAsyncRequestHelpers:
    @pytest.mark.asyncio
    async def test_request_raw_returns_data_and_headers(self, aclient):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value={"key": "value"})
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        data, headers = await aclient._request_raw("GET", f"{aclient.endpoint}/test")
        assert data == {"key": "value"}

    @pytest.mark.asyncio
    async def test_request_returns_data(self, aclient):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value={"result": "ok"})
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        data = await aclient._request("GET", f"{aclient.endpoint}/test")
        assert data == {"result": "ok"}


class TestAsyncClientDigitalTwins:
    @pytest.mark.asyncio
    async def test_get_digital_twin(self, aclient):
        mock_data = {"$dtId": "t1", "$metadata": {"$model": "m1"}}
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        twin = await aclient.get_digital_twin("t1")
        assert isinstance(twin, BasicDigitalTwin)
        assert twin.dtId == "t1"

    @pytest.mark.asyncio
    async def test_upsert_digital_twin(self, aclient):
        twin = BasicDigitalTwin(
            dtId="t2", metadata=DigitalTwinMetadata(model="m1")
        )
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value={"$dtId": "t2", "$metadata": {"$model": "m1"}})
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        result = await aclient.upsert_digital_twin("t2", twin)
        assert result.dtId == "t2"


class TestAsyncClientRelationships:
    @pytest.mark.asyncio
    async def test_get_relationship(self, aclient):
        mock_data = {
            "$relationshipId": "r1", "$sourceId": "t1", "$targetId": "t2",
            "$relationshipName": "contains",
        }
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        rel = await aclient.get_relationship("t1", "r1")
        assert rel.relationshipId == "r1"

    @pytest.mark.asyncio
    async def test_upsert_relationship(self, aclient):
        rel = BasicRelationship(
            relationshipId="", sourceId="", targetId="t2",
            relationshipName="connectedTo",
        )
        mock_data = {
            "$relationshipId": "r2", "$sourceId": "t1", "$targetId": "t2",
            "$relationshipName": "connectedTo",
        }
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_data)
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        result = await aclient.upsert_relationship("t1", "r2", rel)
        assert result.relationshipId == "r2"


class TestAsyncClientQuery:
    @pytest.mark.asyncio
    async def test_query_twins(self, aclient):
        mock_data = {"value": [{"$dtId": "t1", "$metadata": {"$model": "m1"}}]}
        with patch.object(aclient, "_request_raw", return_value=(mock_data, {})):
            results = []
            async for item in aclient.query_twins("SELECT * FROM digitaltwins"):
                results.append(item)
            assert len(results) == 1

    @pytest.mark.asyncio
    async def test_query_twins_passes_parameters(self, aclient):
        """`query_parameters` must be forwarded as `parameters` in the POST body."""
        mock_data = {"value": []}
        params = {"model": "dtmi:com:example:Room;1", "minTemp": 20}
        captured = {}

        async def fake_request_raw(method, url, **kwargs):
            captured["json"] = kwargs.get("json")
            return mock_data, {}

        with patch.object(aclient, "_request_raw", side_effect=fake_request_raw):
            async for _ in aclient.query_twins(
                "SELECT * FROM digitaltwins WHERE $model = $model",
                query_parameters=params,
            ):
                pass
        assert captured["json"]["query"] == "SELECT * FROM digitaltwins WHERE $model = $model"
        assert captured["json"]["parameters"] == params

    @pytest.mark.asyncio
    async def test_query_twins_without_parameters_omits_key(self, aclient):
        mock_data = {"value": []}
        captured = {}

        async def fake_request_raw(method, url, **kwargs):
            captured["json"] = kwargs.get("json")
            return mock_data, {}

        with patch.object(aclient, "_request_raw", side_effect=fake_request_raw):
            async for _ in aclient.query_twins("SELECT * FROM digitaltwins"):
                pass
        assert "parameters" not in captured["json"]
        assert captured["json"]["query"] == "SELECT * FROM digitaltwins"


class TestAsyncClientModels:
    @pytest.mark.asyncio
    async def test_get_model(self, aclient):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value={"id": "m1", "decommissioned": False})
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        model = await aclient.get_model("m1")
        assert model.id == "m1"

    @pytest.mark.asyncio
    async def test_create_models(self, aclient):
        from konnektr_graph.types import DtdlInterface
        iface = DtdlInterface(id="dtmi:com:example:Room;1", type="Interface")
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=[{"id": "dtmi:com:example:Room;1", "decommissioned": False}])
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        models = await aclient.create_models([iface])
        assert len(models) == 1

    @pytest.mark.asyncio
    async def test_delete_all_models(self, aclient):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.status = 204
        mock_resp.headers = {}
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        assert await aclient.delete_all_models() is None
        assert mock_session.request.call_args[0][0] == "DELETE"
        assert mock_session.request.call_args[0][1] == f"{aclient.endpoint}/models"

    @pytest.mark.asyncio
    async def test_search_models_with_vector(self, aclient):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=[{"id": "m1"}])
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        results = await aclient.search_models("room", vector=[0.1, 0.2])
        assert len(results) == 1


class TestAsyncClientErrors:
    @pytest.mark.asyncio
    async def test_404_raises_resource_not_found(self, aclient):
        mock_resp = MagicMock()
        mock_resp.ok = False
        mock_resp.status = 404
        mock_resp.json = AsyncMock(return_value={"error": "Not Found"})
        mock_resp.text = AsyncMock(return_value="Not Found")
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        with pytest.raises(ResourceNotFoundError):
            await aclient.get_digital_twin("missing")

    @pytest.mark.asyncio
    async def test_409_raises_resource_exists(self, aclient):
        mock_resp = MagicMock()
        mock_resp.ok = False
        mock_resp.status = 409
        mock_resp.json = AsyncMock(return_value={"error": "Conflict"})
        mock_resp.text = AsyncMock(return_value="Conflict")
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        with pytest.raises(ResourceExistsError):
            await aclient.get_digital_twin("existing")

    @pytest.mark.asyncio
    async def test_401_raises_authentication_error(self, aclient):
        mock_resp = MagicMock()
        mock_resp.ok = False
        mock_resp.status = 401
        mock_resp.json = AsyncMock(return_value={"error": "Unauthorized"})
        mock_resp.text = AsyncMock(return_value="Unauthorized")
        mock_resp.__aenter__.return_value = mock_resp
        mock_session = MagicMock()
        mock_session.request.return_value = mock_resp
        aclient._session = mock_session
        with pytest.raises(AuthenticationError):
            await aclient.get_digital_twin("unauth")


class TestAsyncPagedIterator:
    @pytest.mark.asyncio
    async def test_single_page(self, aclient):
        mock_data = {"value": [1, 2, 3]}
        with patch.object(aclient, "_request_raw", return_value=(mock_data, {})):
            it = AsyncPagedIterator(aclient, f"{aclient.endpoint}/items")
            results = [item async for item in it]
            assert results == [1, 2, 3]

    @pytest.mark.asyncio
    async def test_next_link_pagination(self, aclient):
        page1 = {"value": [1, 2], "nextLink": "/items?page=2"}
        page2 = {"value": [3, 4]}
        with patch.object(
            aclient, "_request_raw",
            side_effect=[(page1, {}), (page2, {})],
        ) as mock_request:
            it = AsyncPagedIterator(aclient, f"{aclient.endpoint}/items")
            results = [item async for item in it]
            assert results == [1, 2, 3, 4]
            assert mock_request.call_count == 2

    @pytest.mark.asyncio
    async def test_continuation_token(self, aclient):
        page1 = {"value": ["a", "b"]}
        page2 = {"value": ["c"]}
        with patch.object(
            aclient, "_request_raw",
            side_effect=[(page1, {"x-ms-continuation": "tok1"}), (page2, {})],
        ):
            it = AsyncPagedIterator(aclient, f"{aclient.endpoint}/items")
            results = [item async for item in it]
            assert results == ["a", "b", "c"]

    @pytest.mark.asyncio
    async def test_empty_response(self, aclient):
        with patch.object(aclient, "_request_raw", return_value=({"value": []}, {})):
            it = AsyncPagedIterator(aclient, f"{aclient.endpoint}/items")
            results = [item async for item in it]
            assert results == []

    @pytest.mark.asyncio
    async def test_model_cls(self, aclient):
        mock_data = {
            "value": [{
                "id": "job1", "status": "running",
                "inputBlobUri": "https://blob/in", "outputBlobUri": "https://blob/out",
                "createdDateTime": "2024-01-01T00:00:00Z",
            }]
        }
        with patch.object(aclient, "_request_raw", return_value=(mock_data, {})):
            it = AsyncPagedIterator(aclient, f"{aclient.endpoint}/jobs/import", model_cls=ImportJob)
            results = [item async for item in it]
            assert len(results) == 1
            assert isinstance(results[0], ImportJob)
