import json
from unittest.mock import MagicMock, patch

import pytest
import requests

from konnektr_graph.client import KonnektrGraphClient, PagedIterator
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


def make_mock_response(status_code=200, json_data=None, headers=None):
    mock = MagicMock(spec=requests.Response)
    mock.status_code = status_code
    mock.ok = 200 <= status_code < 300
    mock.json.return_value = json_data or {}
    mock.headers = headers or {}
    return mock


class TestKonnektrGraphClientInit:
    def test_endpoint_normalized(self, credential):
        client = KonnektrGraphClient("graph.konnektr.io", credential)
        assert client.endpoint == "https://graph.konnektr.io"

    def test_endpoint_https_preserved(self, credential):
        client = KonnektrGraphClient("https://graph.konnektr.io", credential)
        assert client.endpoint == "https://graph.konnektr.io"


class TestKonnektrGraphClientAuth:
    def test_authorization_header_added(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(json_data={"$dtId": "t1", "$metadata": {"$model": "m1"}})
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.get_digital_twin("t1")
            call_headers = mock_req.call_args[1]["headers"]
            assert "Authorization" in call_headers
            assert call_headers["Authorization"] == "Bearer test-token-12345"


class TestKonnektrGraphClientDigitalTwins:
    def test_get_digital_twin(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {
            "$dtId": "twin1",
            "$metadata": {"$model": "dtmi:com:example:Room;1"},
        }
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(requests, "request", return_value=mock_resp):
            twin = client.get_digital_twin("twin1")
            assert isinstance(twin, BasicDigitalTwin)
            assert twin.dtId == "twin1"

    def test_upsert_digital_twin(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        twin = BasicDigitalTwin(
            dtId="twin2",
            metadata=DigitalTwinMetadata(model="dtmi:com:example:Room;1"),
        )
        mock_resp = make_mock_response(
            json_data={
                "$dtId": "twin2",
                "$metadata": {"$model": "dtmi:com:example:Room;1"},
            }
        )
        with patch.object(requests, "request", return_value=mock_resp):
            result = client.upsert_digital_twin("twin2", twin)
            assert result.dtId == "twin2"

    def test_update_digital_twin(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response()
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.update_digital_twin("twin1", [{"op": "replace", "path": "/temperature", "value": 80}])
            call = mock_req.call_args
            assert call[0][0] == "PATCH"
            assert call[1]["headers"]["Content-Type"] == "application/json-patch+json"

    def test_delete_digital_twin(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response()
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.delete_digital_twin("twin1")
            assert mock_req.call_args[0][0] == "DELETE"


class TestKonnektrGraphClientComponents:
    def test_get_component(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {"$metadata": {"$model": "dtmi:com:example:Thermostat;1"}, "temp": 75}
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(requests, "request", return_value=mock_resp):
            comp = client.get_component("twin1", "thermostat")
            assert comp.properties["temp"] == 75

    def test_update_component(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response()
        patch_ops = [{"op": "replace", "path": "/temp", "value": 80}]
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.update_component("twin1", "thermostat", patch_ops)
            assert mock_req.call_args[0][0] == "PATCH"


class TestKonnektrGraphClientRelationships:
    def test_get_relationship(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {
            "$relationshipId": "rel1",
            "$sourceId": "twin1",
            "$targetId": "twin2",
            "$relationshipName": "contains",
        }
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(requests, "request", return_value=mock_resp):
            rel = client.get_relationship("twin1", "rel1")
            assert rel.relationshipId == "rel1"

    def test_upsert_relationship(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        rel = BasicRelationship(
            relationshipId="", sourceId="", targetId="twinB",
            relationshipName="connectedTo",
        )
        mock_resp = make_mock_response(
            json_data={
                "$relationshipId": "rel2",
                "$sourceId": "twinA",
                "$targetId": "twinB",
                "$relationshipName": "connectedTo",
            }
        )
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            with patch.object(client, "_request", return_value=mock_resp):
                result = client.upsert_relationship("twinA", "rel2", rel)
                assert result["$relationshipId"] == "rel2"

    def test_delete_relationship(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response()
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.delete_relationship("twin1", "rel1")
            assert mock_req.call_args[0][0] == "DELETE"

    def test_list_relationships(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {
            "value": [
                {"$relationshipId": "r1", "$sourceId": "twin1", "$targetId": "twin2", "$relationshipName": "contains"},
            ]
        }
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(client, "_request", return_value=mock_resp):
            it = client.list_relationships("twin1")
            results = list(it)
            assert len(results) == 1
            assert results[0].relationshipId == "r1"


class TestKonnektrGraphClientQuery:
    def test_query_twins(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {"value": [{"$dtId": "t1", "$metadata": {"$model": "m1"}}]}
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(client, "_request", return_value=mock_resp):
            it = client.query_twins("SELECT * FROM digitaltwins")
            results = list(it)
            assert len(results) == 1
            assert results[0]["$dtId"] == "t1"

    def test_query_twins_with_max_items(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(json_data={"value": []})
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            list(client.query_twins("SELECT *", max_items_per_page=50))
            call_headers = mock_req.call_args[1]["headers"]
            assert call_headers["max-items-per-page"] == "50"

    def test_query_twins_passes_parameters(self, credential, endpoint):
        """The `query_parameters` dict must be forwarded as `parameters` in the POST body."""
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(json_data={"value": []})
        params = {"model": "dtmi:com:example:Room;1", "minTemp": 20}
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            list(client.query_twins("SELECT * FROM digitaltwins WHERE $model = $model", query_parameters=params))
            call_body = mock_req.call_args[1]["json"]
            assert call_body["query"] == "SELECT * FROM digitaltwins WHERE $model = $model"
            assert call_body["parameters"] == params

    def test_query_twins_without_parameters_omits_key(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(json_data={"value": []})
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            list(client.query_twins("SELECT * FROM digitaltwins"))
            call_body = mock_req.call_args[1]["json"]
            assert "parameters" not in call_body
            assert call_body["query"] == "SELECT * FROM digitaltwins"


class TestKonnektrGraphClientModels:
    def test_get_model(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {"id": "dtmi:com:example:Room;1", "decommissioned": False}
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(requests, "request", return_value=mock_resp):
            model = client.get_model("dtmi:com:example:Room;1")
            assert model.id == "dtmi:com:example:Room;1"

    def test_list_models(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {"value": [{"id": "m1", "decommissioned": False}]}
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(client, "_request", return_value=mock_resp):
            results = list(client.list_models())
            assert len(results) == 1

    def test_create_models(self, credential, endpoint):
        from konnektr_graph.types import DtdlInterface
        client = KonnektrGraphClient(endpoint, credential)
        iface = DtdlInterface(id="dtmi:com:example:Room;1", type="Interface")
        mock_resp = make_mock_response(
            json_data=[{"id": "dtmi:com:example:Room;1", "decommissioned": False}]
        )
        with patch.object(requests, "request", return_value=mock_resp):
            models = client.create_models([iface])
            assert len(models) == 1
            assert models[0].id == "dtmi:com:example:Room;1"

    def test_decommission_model(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response()
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.decommission_model("dtmi:com:example:Room;1")
            assert mock_req.call_args[0][0] == "PATCH"

    def test_delete_model(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response()
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.delete_model("dtmi:com:example:Room;1")
            assert mock_req.call_args[0][0] == "DELETE"

    def test_delete_all_models(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response()
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.delete_all_models()
            assert mock_req.call_args[0][0] == "DELETE"
            assert mock_req.call_args[0][1] == f"{client.endpoint}/models"

    def test_search_models(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(json_data=[{"id": "m1"}])
        with patch.object(requests, "request", return_value=mock_resp):
            results = client.search_models("temperature")
            assert len(results) == 1

    def test_search_models_with_vector(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(json_data=[{"id": "m1"}])
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.search_models("temperature", vector=[0.1, 0.2])
            body = mock_req.call_args[1]["json"]
            assert "vector" in body


class TestKonnektrGraphClientSearchTwins:
    def test_search_twins(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(json_data=[{"$dtId": "t1"}])
        with patch.object(requests, "request", return_value=mock_resp):
            results = client.search_twins(vector=[0.1, 0.2])
            assert len(results) == 1

    def test_search_twins_with_model_filter(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(json_data=[])
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.search_twins(vector=[0.1], model_filter="dtmi:com:example:Room;1")
            body = mock_req.call_args[1]["json"]
            assert body["modelFilter"] == "dtmi:com:example:Room;1"


class TestKonnektrGraphClientTelemetry:
    def test_publish_telemetry(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response()
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.publish_telemetry("twin1", {"temp": 75})
            assert mock_req.call_args[0][0] == "POST"

    def test_publish_telemetry_with_message_id(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response()
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.publish_telemetry("twin1", {"temp": 75}, message_id="msg-1")
            assert mock_req.call_args[1]["headers"]["Message-Id"] == "msg-1"

    def test_publish_component_telemetry(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response()
        with patch.object(requests, "request", return_value=mock_resp) as mock_req:
            client.publish_component_telemetry("twin1", "thermostat", {"temp": 75})
            assert mock_req.call_args[0][0] == "POST"


class TestKonnektrGraphClientImportJobs:
    def test_list_import_jobs(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {
            "value": [{
                "id": "job1", "status": "completed",
                "inputBlobUri": "https://blob/in", "outputBlobUri": "https://blob/out",
                "createdDateTime": "2024-01-01T00:00:00Z",
            }]
        }
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(client, "_request", return_value=mock_resp):
            results = list(client.list_import_jobs())
            assert len(results) == 1
            assert isinstance(results[0], ImportJob)

    def test_get_import_job(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {
            "id": "job1", "status": "completed",
            "inputBlobUri": "https://blob/in", "outputBlobUri": "https://blob/out",
            "createdDateTime": "2024-01-01T00:00:00Z",
        }
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(requests, "request", return_value=mock_resp):
            job = client.get_import_job("job1")
            assert job.id == "job1"

    def test_create_import_job(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {
            "id": "job1", "status": "notstarted",
            "inputBlobUri": "https://blob/in", "outputBlobUri": "https://blob/out",
            "createdDateTime": "2024-01-01T00:00:00Z",
        }
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(requests, "request", return_value=mock_resp):
            job = client.create_import_job("job1", {})
            assert job.id == "job1"

    def test_cancel_import_job(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {
            "id": "job1", "status": "cancelling",
            "inputBlobUri": "https://blob/in", "outputBlobUri": "https://blob/out",
            "createdDateTime": "2024-01-01T00:00:00Z",
        }
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(requests, "request", return_value=mock_resp):
            job = client.cancel_import_job("job1")
            assert job.status == "cancelling"


class TestKonnektrGraphClientDeleteJobs:
    def test_list_delete_jobs(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {
            "value": [{"id": "del1", "status": "running", "createdDateTime": "2024-01-01T00:00:00Z"}]
        }
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(client, "_request", return_value=mock_resp):
            results = list(client.list_delete_jobs())
            assert len(results) == 1

    def test_get_delete_job(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {"id": "del1", "status": "completed", "createdDateTime": "2024-01-01T00:00:00Z"}
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(requests, "request", return_value=mock_resp):
            job = client.get_delete_job("del1")
            assert job.id == "del1"

    def test_create_delete_job(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {"id": "del1", "status": "notstarted", "createdDateTime": "2024-01-01T00:00:00Z"}
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(requests, "request", return_value=mock_resp):
            job = client.create_delete_job("del1")
            assert job.id == "del1"


class TestKonnektrGraphClientErrors:
    def test_404_raises_resource_not_found(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(status_code=404)
        with pytest.raises(ResourceNotFoundError):
            client._handle_error(mock_resp)

    def test_409_raises_resource_exists(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(status_code=409)
        with pytest.raises(ResourceExistsError):
            client._handle_error(mock_resp)

    def test_401_raises_authentication_error(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(status_code=401)
        with pytest.raises(AuthenticationError):
            client._handle_error(mock_resp)

    def test_403_raises_authentication_error(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(status_code=403)
        with pytest.raises(AuthenticationError):
            client._handle_error(mock_resp)

    def test_500_raises_http_response_error(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(status_code=500, json_data={"error": "Internal"})
        with pytest.raises(HttpResponseError):
            client._handle_error(mock_resp)


class TestPagedIterator:
    def test_single_page(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {"value": [1, 2, 3]}
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(client, "_request", return_value=mock_resp):
            it = PagedIterator(client, f"{endpoint}/items")
            results = list(it)
            assert results == [1, 2, 3]

    def test_next_link_pagination(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        page1 = make_mock_response(json_data={"value": [1, 2], "nextLink": f"{endpoint}/items?page=2"})
        page2 = make_mock_response(json_data={"value": [3, 4]})
        with patch.object(
            client, "_request", side_effect=[page1, page2]
        ) as mock_request:
            it = PagedIterator(client, f"{endpoint}/items")
            results = list(it)
            assert results == [1, 2, 3, 4]
            assert mock_request.call_count == 2

    def test_continuation_token_pagination(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        page1 = make_mock_response(
            json_data={"value": ["a", "b"]},
            headers={"x-ms-continuation": "token123"},
        )
        page2 = make_mock_response(json_data={"value": ["c"]})
        with patch.object(client, "_request", side_effect=[page1, page2]) as mock_request:
            it = PagedIterator(client, f"{endpoint}/items")
            results = list(it)
            assert results == ["a", "b", "c"]
            assert mock_request.call_count == 2

    def test_continuation_token_in_body(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        page1 = make_mock_response(json_data={"value": ["x"], "continuationToken": "ct1"})
        page2 = make_mock_response(json_data={"value": ["y"]})
        with patch.object(client, "_request", side_effect=[page1, page2]):
            it = PagedIterator(client, f"{endpoint}/items")
            results = list(it)
            assert results == ["x", "y"]

    def test_empty_response(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_resp = make_mock_response(json_data={"value": []})
        with patch.object(client, "_request", return_value=mock_resp):
            it = PagedIterator(client, f"{endpoint}/items")
            results = list(it)
            assert results == []

    def test_model_cls(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        mock_data = {
            "value": [{
                "id": "job1", "status": "running",
                "inputBlobUri": "https://blob/in", "outputBlobUri": "https://blob/out",
                "createdDateTime": "2024-01-01T00:00:00Z",
            }]
        }
        mock_resp = make_mock_response(json_data=mock_data)
        with patch.object(client, "_request", return_value=mock_resp):
            it = PagedIterator(client, f"{endpoint}/jobs/import", model_cls=ImportJob)
            results = list(it)
            assert len(results) == 1
            assert isinstance(results[0], ImportJob)

    def test_relative_next_link(self, credential, endpoint):
        client = KonnektrGraphClient(endpoint, credential)
        page1 = make_mock_response(json_data={"value": [1], "nextLink": "/items?page=2"})
        page2 = make_mock_response(json_data={"value": [2]})
        with patch.object(client, "_request", side_effect=[page1, page2]) as mock_request:
            it = PagedIterator(client, f"{endpoint}/items")
            results = list(it)
            assert results == [1, 2]
            second_url = mock_request.call_args_list[1][0][1]
            assert second_url.startswith(endpoint)
