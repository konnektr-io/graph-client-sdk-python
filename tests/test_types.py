from konnektr_graph.types import (
    BasicDigitalTwin,
    BasicDigitalTwinComponent,
    BasicRelationship,
    DigitalTwinMetadata,
    DtdlArraySchema,
    DtdlComponent,
    DtdlEnumSchema,
    DtdlEnumValue,
    DtdlInterface,
    DtdlMapKey,
    DtdlMapSchema,
    DtdlMapValue,
    DtdlObjectField,
    DtdlObjectSchema,
    DtdlProperty,
    DtdlRelationship,
    DtdlTelemetry,
)


class TestBasicDigitalTwin:
    def test_from_dict_minimal(self):
        data = {
            "$dtId": "twin1",
            "$metadata": {"$model": "dtmi:com:example:Room;1"},
        }
        twin = BasicDigitalTwin.from_dict(data)
        assert twin.dtId == "twin1"
        assert twin.metadata.model == "dtmi:com:example:Room;1"
        assert twin.metadata.metadata == {}
        assert twin.etag is None
        assert twin.lastUpdateTime is None
        assert twin.contents == {}

    def test_from_dict_full(self):
        data = {
            "$dtId": "twin2",
            "$metadata": {
                "$model": "dtmi:com:example:Room;1",
                "$lastUpdateTime": "2024-01-01T00:00:00Z",
            },
            "$etag": "W/\"abc123\"",
            "temperature": 72.5,
            "humidity": 50,
        }
        twin = BasicDigitalTwin.from_dict(data)
        assert twin.dtId == "twin2"
        assert twin.etag == 'W/"abc123"'
        assert twin.lastUpdateTime == "2024-01-01T00:00:00Z"
        assert twin.contents == {"temperature": 72.5, "humidity": 50}

    def test_to_dict_roundtrip(self):
        original = BasicDigitalTwin(
            dtId="twin3",
            metadata=DigitalTwinMetadata(model="dtmi:com:example:Room;1"),
            etag='W/"xyz"',
            contents={"speed": 100},
        )
        as_dict = original.to_dict()
        restored = BasicDigitalTwin.from_dict(as_dict)
        assert restored.dtId == original.dtId
        assert restored.metadata.model == original.metadata.model
        assert restored.etag == original.etag
        assert restored.contents == original.contents


class TestBasicRelationship:
    def test_from_dict_minimal(self):
        data = {
            "$relationshipId": "rel1",
            "$sourceId": "twin1",
            "$targetId": "twin2",
            "$relationshipName": "contains",
        }
        rel = BasicRelationship.from_dict(data)
        assert rel.relationshipId == "rel1"
        assert rel.sourceId == "twin1"
        assert rel.targetId == "twin2"
        assert rel.relationshipName == "contains"
        assert rel.etag is None
        assert rel.properties == {}

    def test_from_dict_with_properties(self):
        data = {
            "$relationshipId": "rel2",
            "$sourceId": "twinA",
            "$targetId": "twinB",
            "$relationshipName": "connectedTo",
            "$etag": "W/\"etag123\"",
            "weight": 10,
            "label": "main",
        }
        rel = BasicRelationship.from_dict(data)
        assert rel.relationshipId == "rel2"
        assert rel.etag == 'W/"etag123"'
        assert rel.properties == {"weight": 10, "label": "main"}

    def test_to_dict_roundtrip(self):
        original = BasicRelationship(
            relationshipId="rel3",
            sourceId="twinX",
            targetId="twinY",
            relationshipName="feeds",
            etag='W/"etag456"',
            properties={"flowRate": 50},
        )
        as_dict = original.to_dict()
        restored = BasicRelationship.from_dict(as_dict)
        assert restored.relationshipId == original.relationshipId
        assert restored.sourceId == original.sourceId
        assert restored.targetId == original.targetId
        assert restored.relationshipName == original.relationshipName
        assert restored.etag == original.etag
        assert restored.properties == original.properties


class TestBasicDigitalTwinComponent:
    def test_from_dict(self):
        data = {
            "$metadata": {"$model": "dtmi:com:example:Thermostat;1"},
            "temperature": 75.0,
        }
        comp = BasicDigitalTwinComponent.from_dict(data)
        assert comp.metadata == {"$model": "dtmi:com:example:Thermostat;1"}
        assert comp.properties == {"temperature": 75.0}

    def test_to_dict_roundtrip(self):
        original = BasicDigitalTwinComponent(
            metadata={"$model": "dtmi:com:example:Thermostat;1"},
            properties={"humidity": 45},
        )
        as_dict = original.to_dict()
        restored = BasicDigitalTwinComponent.from_dict(as_dict)
        assert restored.metadata == original.metadata
        assert restored.properties == original.properties


class TestDigitalTwinMetadata:
    def test_creation(self):
        meta = DigitalTwinMetadata(model="dtmi:com:example:Room;1")
        assert meta.model == "dtmi:com:example:Room;1"
        assert meta.metadata == {}

    def test_with_additional(self):
        meta = DigitalTwinMetadata(
            model="dtmi:com:example:Room;1",
            metadata={"customProp": "value"},
        )
        assert meta.metadata == {"customProp": "value"}


class TestDtdlEnumValue:
    def test_from_dict(self):
        data = {"name": "Low", "enumValue": 0}
        v = DtdlEnumValue.from_dict(data)
        assert v.name == "Low"
        assert v.enumValue == 0

    def test_to_dict_roundtrip(self):
        original = DtdlEnumValue(name="High", enumValue=1, displayName="High value")
        as_dict = original.to_dict()
        restored = DtdlEnumValue.from_dict(as_dict)
        assert restored.name == original.name


class TestDtdlEnumSchema:
    def test_from_dict(self):
        data = {
            "@type": "Enum",
            "enumValues": [{"name": "Low", "enumValue": 0}],
            "valueSchema": "integer",
        }
        schema = DtdlEnumSchema.from_dict(data)
        assert schema.type == "Enum"
        assert len(schema.enumValues) == 1
        assert schema.enumValues[0].name == "Low"

    def test_to_dict_roundtrip(self):
        original = DtdlEnumSchema(
            type="Enum",
            enumValues=[DtdlEnumValue(name="Off", enumValue=0)],
            valueSchema="integer",
        )
        as_dict = original.to_dict()
        restored = DtdlEnumSchema.from_dict(as_dict)
        assert len(restored.enumValues) == 1


class TestDtdlMapSchema:
    def test_from_dict(self):
        data = {
            "@type": "Map",
            "mapKey": {"name": "key", "schema": "string"},
            "mapValue": {"name": "value", "schema": "string"},
        }
        m = DtdlMapSchema.from_dict(data)
        assert m.mapKey.name == "key"
        assert m.mapValue.name == "value"

    def test_to_dict_roundtrip(self):
        original = DtdlMapSchema(
            type="Map",
            mapKey=DtdlMapKey(name="k", schema="string"),
            mapValue=DtdlMapValue(name="v", schema="string"),
        )
        as_dict = original.to_dict()
        restored = DtdlMapSchema.from_dict(as_dict)
        assert restored.mapKey.name == "k"


class TestDtdlObjectSchema:
    def test_from_dict(self):
        data = {
            "@type": "Object",
            "fields": [{"name": "x", "schema": "double"}],
        }
        obj = DtdlObjectSchema.from_dict(data)
        assert len(obj.fields) == 1
        assert obj.fields[0].name == "x"

    def test_to_dict_roundtrip(self):
        original = DtdlObjectSchema(
            type="Object",
            fields=[DtdlObjectField(name="y", schema="integer")]
        )
        as_dict = original.to_dict()
        restored = DtdlObjectSchema.from_dict(as_dict)
        assert restored.fields[0].name == "y"


class TestDtdlArraySchema:
    def test_from_dict(self):
        data = {"@type": "Array", "elementSchema": "double"}
        arr = DtdlArraySchema.from_dict(data)
        assert arr.elementSchema == "double"

    def test_to_dict_roundtrip(self):
        original = DtdlArraySchema(type="Array", elementSchema="double")
        as_dict = original.to_dict()
        restored = DtdlArraySchema.from_dict(as_dict)
        assert restored.elementSchema == "double"


class TestDtdlProperty:
    def test_from_dict(self):
        data = {"name": "temperature", "schema": "double", "@type": "Property"}
        p = DtdlProperty.from_dict(data)
        assert p.name == "temperature"
        assert p.schema == "double"

    def test_to_dict_roundtrip(self):
        original = DtdlProperty(name="humidity", schema="double", type="Property")
        as_dict = original.to_dict()
        restored = DtdlProperty.from_dict(as_dict)
        assert restored.name == "humidity"

    def test_from_dict_missing_schema(self):
        """Should not crash if schema is missing, defaulting to 'string'."""
        data = {"name": "broken", "@type": "Property"}
        p = DtdlProperty.from_dict(data)
        assert p.name == "broken"
        assert p.schema == "string"

    def test_relationship_from_dict_missing_target(self):
        """Should not crash if relationship target is missing."""
        data = {"name": "brokenRel", "@type": "Relationship"}
        r = DtdlRelationship.from_dict(data)
        assert r.name == "brokenRel"
        assert r.target == ""


class TestDtdlRelationship:
    def test_from_dict(self):
        data = {
            "name": "contains",
            "@type": "Relationship",
            "target": "dtmi:com:example:Room;1",
            "properties": [],
        }
        r = DtdlRelationship.from_dict(data)
        assert r.name == "contains"
        assert r.target == "dtmi:com:example:Room;1"

    def test_to_dict_roundtrip(self):
        original = DtdlRelationship(
            name="feeds", type="Relationship", target="dtmi:com:example:Device;1", properties=[]
        )
        as_dict = original.to_dict()
        restored = DtdlRelationship.from_dict(as_dict)
        assert restored.name == "feeds"


class TestDtdlTelemetry:
    def test_from_dict(self):
        data = {"name": "temp", "schema": "double", "@type": "Telemetry"}
        t = DtdlTelemetry.from_dict(data)
        assert t.name == "temp"

    def test_to_dict_roundtrip(self):
        original = DtdlTelemetry(name="pressure", schema="double", type="Telemetry")
        as_dict = original.to_dict()
        restored = DtdlTelemetry.from_dict(as_dict)
        assert restored.name == "pressure"


class TestDtdlComponent:
    def test_from_dict(self):
        data = {
            "name": "thermostat",
            "schema": "dtmi:com:example:Thermostat;1",
            "@type": "Component",
        }
        c = DtdlComponent.from_dict(data)
        assert c.name == "thermostat"
        assert c.schema == "dtmi:com:example:Thermostat;1"

    def test_to_dict_roundtrip(self):
        original = DtdlComponent(
            name="sensor", type="Component", schema="dtmi:com:example:Sensor;1"
        )
        as_dict = original.to_dict()
        restored = DtdlComponent.from_dict(as_dict)
        assert restored.name == "sensor"


class TestDtdlInterface:
    def test_from_dict_minimal(self):
        data = {
            "@id": "dtmi:com:example:Room;1",
            "@type": "Interface",
        }
        iface = DtdlInterface.from_dict(data)
        assert iface.id == "dtmi:com:example:Room;1"
        assert iface.contents is None

    def test_from_dict_with_contents(self):
        data = {
            "@id": "dtmi:com:example:Room;1",
            "@type": "Interface",
            "contents": [
                {"name": "temp", "schema": "double", "@type": "Property"},
                {"name": "contains", "@type": "Relationship", "target": "dtmi:com:example:Device;1", "properties": []},
            ],
        }
        iface = DtdlInterface.from_dict(data)
        assert iface.id == "dtmi:com:example:Room;1"
        assert len(iface.contents) == 2

    def test_to_dict_roundtrip(self):
        original = DtdlInterface(
            id="dtmi:com:example:Device;1",
            type="Interface",
            displayName="Device",
        )
        as_dict = original.to_dict()
        restored = DtdlInterface.from_dict(as_dict)
        assert restored.id == original.id
        assert restored.displayName == original.displayName

    def test_normalize_keys(self):
        data = {
            "@id": "dtmi:com:example:Room;1",
            "@type": "Interface",
            "displayName": {"en": "Room"},
        }
        iface = DtdlInterface.from_dict(data)
        assert iface.displayName == {"en": "Room"}


class TestDtdlInterfaceSchemas:
    """DTDL v4 'schemas' (reusable named complex schemas) + languageVersion/annotations."""

    def _v4_sensor_model(self) -> dict:
        # A DTDL v4 interface with two reusable named schemas referenced by DTMI.
        return {
            "@id": "dtmi:com:example:Sensor;1",
            "@type": "Interface",
            "@context": "dtmi:dtdl:context;4",
            "languageVersion": 1,
            "annotations": {"recommended": True},
            "contents": [
                {
                    "@type": "Property",
                    "name": "status",
                    "schema": "dtmi:com:example:Status;1",
                },
                {
                    "@type": "Property",
                    "name": "location",
                    "schema": "dtmi:com:example:Geo;1",
                },
            ],
            "schemas": [
                {
                    "@id": "dtmi:com:example:Status;1",
                    "@type": "Enum",
                    "valueSchema": "string",
                    "enumValues": [
                        {"name": "On", "enumValue": "on"},
                        {"name": "Off", "enumValue": "off"},
                    ],
                },
                {
                    "@id": "dtmi:com:example:Geo;1",
                    "@type": "Object",
                    "fields": [
                        {"name": "lat", "schema": "double"},
                        {"name": "lon", "schema": "double"},
                    ],
                },
            ],
        }

    def test_from_dict_parses_schemas(self):
        iface = DtdlInterface.from_dict(self._v4_sensor_model())
        assert iface.schemas is not None
        assert len(iface.schemas) == 2
        by_id = {s["@id"]: s for s in iface.schemas}
        assert "dtmi:com:example:Status;1" in by_id
        assert by_id["dtmi:com:example:Status;1"]["@type"] == "Enum"
        assert (
            by_id["dtmi:com:example:Status;1"]["enumValues"][0]["name"] == "On"
        )
        assert by_id["dtmi:com:example:Geo;1"]["fields"][1]["name"] == "lon"

    def test_to_dict_emits_schemas(self):
        iface = DtdlInterface.from_dict(self._v4_sensor_model())
        d = iface.to_dict()
        assert "schemas" in d
        assert len(d["schemas"]) == 2
        # Contents still reference the named schemas by DTMI (lossless).
        schemas_referenced = {c["schema"] for c in d["contents"]}
        assert "dtmi:com:example:Status;1" in schemas_referenced

    def test_roundtrip_preserves_schemas(self):
        original = self._v4_sensor_model()
        iface = DtdlInterface.from_dict(original)
        restored = DtdlInterface.from_dict(iface.to_dict())
        assert restored.schemas == iface.schemas
        assert restored.contents == iface.contents
        assert restored.languageVersion == 1
        assert restored.annotations == {"recommended": True}

    def test_single_schema_dict_is_wrapped(self):
        data = {
            "@id": "dtmi:com:example:Thing;1",
            "@type": "Interface",
            "schemas": {
                "@id": "dtmi:com:example:Color;1",
                "@type": "Enum",
                "valueSchema": "string",
                "enumValues": [{"name": "Red", "enumValue": "red"}],
            },
        }
        iface = DtdlInterface.from_dict(data)
        assert isinstance(iface.schemas, list)
        assert len(iface.schemas) == 1
        assert iface.schemas[0]["@id"] == "dtmi:com:example:Color;1"

    def test_backward_compat_omits_schemas_when_absent(self):
        data = {"@id": "dtmi:com:example:Room;1", "@type": "Interface"}
        iface = DtdlInterface.from_dict(data)
        assert iface.schemas is None
        assert "schemas" not in iface.to_dict()
        assert iface.languageVersion is None
        assert iface.annotations is None
