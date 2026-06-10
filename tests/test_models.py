from konnektr_graph.models import DeleteJob, DigitalTwinsModelData, ImportJob


class TestImportJob:
    def test_from_dict_minimal(self):
        data = {
            "id": "job1",
            "status": "notstarted",
            "inputBlobUri": "https://blob/input",
            "outputBlobUri": "https://blob/output",
            "createdDateTime": "2024-01-01T00:00:00Z",
        }
        job = ImportJob.from_dict(data)
        assert job.id == "job1"
        assert job.status == "notstarted"
        assert job.error is None
        assert job.last_action_date_time is None

    def test_from_dict_full(self):
        data = {
            "id": "job2",
            "status": "completed",
            "inputBlobUri": "https://blob/in",
            "outputBlobUri": "https://blob/out",
            "createdDateTime": "2024-01-01T00:00:00Z",
            "lastActionDateTime": "2024-01-02T00:00:00Z",
            "finishedDateTime": "2024-01-02T01:00:00Z",
            "purgeDateTime": "2024-02-01T00:00:00Z",
            "error": {"code": "Timeout", "message": "Job timed out"},
        }
        job = ImportJob.from_dict(data)
        assert job.status == "completed"
        assert job.error == {"code": "Timeout", "message": "Job timed out"}
        assert job.finished_date_time == "2024-01-02T01:00:00Z"

    def test_to_dict_roundtrip(self):
        original = ImportJob(
            id="job3",
            status="running",
            input_blob_uri="https://blob/in",
            output_blob_uri="https://blob/out",
            created_date_time="2024-01-01T00:00:00Z",
        )
        as_dict = original.to_dict()
        restored = ImportJob.from_dict(as_dict)
        assert restored.id == original.id
        assert restored.status == original.status

    def test_to_dict_includes_optionals(self):
        job = ImportJob(
            id="job4",
            status="failed",
            input_blob_uri="https://blob/in",
            output_blob_uri="https://blob/out",
            created_date_time="2024-01-01T00:00:00Z",
            error={"code": "Error", "message": "Something went wrong"},
        )
        as_dict = job.to_dict()
        assert "error" in as_dict
        assert as_dict["error"]["code"] == "Error"


class TestDeleteJob:
    def test_from_dict_minimal(self):
        data = {
            "id": "del1",
            "status": "running",
            "createdDateTime": "2024-01-01T00:00:00Z",
        }
        job = DeleteJob.from_dict(data)
        assert job.id == "del1"
        assert job.status == "running"
        assert job.error is None

    def test_from_dict_full(self):
        data = {
            "id": "del2",
            "status": "completed",
            "createdDateTime": "2024-01-01T00:00:00Z",
            "finishedDateTime": "2024-01-02T00:00:00Z",
            "error": {"code": "Success", "message": "Deleted"},
        }
        job = DeleteJob.from_dict(data)
        assert job.finished_date_time == "2024-01-02T00:00:00Z"

    def test_to_dict_roundtrip(self):
        original = DeleteJob(
            id="del3",
            status="notstarted",
            created_date_time="2024-01-01T00:00:00Z",
        )
        as_dict = original.to_dict()
        restored = DeleteJob.from_dict(as_dict)
        assert restored.id == original.id


class TestDigitalTwinsModelData:
    def test_from_dict_minimal(self):
        data = {
            "id": "dtmi:com:example:Room;1",
            "decommissioned": False,
        }
        model = DigitalTwinsModelData.from_dict(data)
        assert model.id == "dtmi:com:example:Room;1"
        assert model.decommissioned is False
        assert model.model is None

    def test_from_dict_with_model(self):
        data = {
            "id": "dtmi:com:example:Room;1",
            "decommissioned": False,
            "model": {
                "@id": "dtmi:com:example:Room;1",
                "@type": "Interface",
            },
        }
        model = DigitalTwinsModelData.from_dict(data)
        assert model.model is not None
        assert model.model.id == "dtmi:com:example:Room;1"

    def test_from_dict_with_properties(self):
        data = {
            "id": "dtmi:com:example:Room;1",
            "decommissioned": False,
            "properties": [
                {"name": "temp", "schema": "double", "@type": "Property"}
            ],
        }
        model = DigitalTwinsModelData.from_dict(data)
        assert model.properties is not None
        assert len(model.properties) == 1
        assert model.properties[0].name == "temp"

    def test_to_dict_roundtrip(self):
        original = DigitalTwinsModelData(
            id="dtmi:com:example:Room;1",
            decommissioned=False,
            display_name="Room",
        )
        as_dict = original.to_dict()
        restored = DigitalTwinsModelData.from_dict(as_dict)
        assert restored.id == original.id
        assert restored.display_name == original.display_name

    def test_to_dict_excludes_none_fields(self):
        model = DigitalTwinsModelData(id="dtmi:com:example:Room;1")
        as_dict = model.to_dict()
        assert "description" not in as_dict
        assert "displayName" not in as_dict
