# konnektr_graph/types.py
"""
Type definitions and aliases for the Konnektr Graph SDK.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Protocol, TypedDict, Union

# JSON types
JsonValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
JsonObject = Dict[str, JsonValue]
JsonArray = List[JsonValue]

# Digital Twin types
DigitalTwinId = str
ComponentName = str
RelationshipId = str
RelationshipName = str
ModelId = str
MessageId = str

# Job types
JobId = str
JobStatus = Literal[
    "notstarted",
    "notStarted",
    "running",
    "completed",
    "failed",
    "canceling",
    "cancelled",
]

# Patch operations
JsonPatchOperation = TypedDict(
    "JsonPatchOperation",
    {
        "op": Literal["add", "remove", "replace", "move", "copy", "test"],
        "path": str,
        "value": Any,
        "from": str,
    },
    total=False,
)

# Query types
QueryExpression = str


# ============================================================================
# Structured Models (Dataclasses) - for schema generation and validation
# ============================================================================


@dataclass
class DigitalTwinMetadata:
    """
    Metadata for a digital twin.

    Attributes:
        model: The model ID (e.g., dtmi:com:example:Room;1).
        metadata: Additional metadata properties.
    """

    model: ModelId  # Represents $model in JSON
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata


@dataclass
class BasicDigitalTwin:
    """
    A structured digital twin following the Azure Digital Twins BasicDigitalTwin pattern.

    This class provides proper typing and validation for digital twin data,
    making it compatible with MCP schema generation for LLMs.

    Attributes:
        dtId: The unique ID of the digital twin.
        metadata: Information about the model this twin conforms to.
        etag: Optional ETag for concurrency control.
        lastUpdateTime: Optional timestamp of last update.
        contents: Additional properties defined in the DTDL model.
    """

    dtId: DigitalTwinId  # Represents $dtId in JSON
    metadata: DigitalTwinMetadata  # Represents $metadata in JSON
    etag: Optional[str] = None  # Represents $etag in JSON
    lastUpdateTime: Optional[str] = None  # Represents $lastUpdateTime in JSON
    contents: Dict[str, Any] = field(
        default_factory=dict
    )  # Custom properties and components

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BasicDigitalTwin":
        """Create a BasicDigitalTwin from a dictionary with $ prefixed keys."""
        metadata_data: Dict[str, Any] = data.get("$metadata", {})
        model_str = metadata_data.get("$model", "")
        # Extract additional metadata (non-$model, non-$lastUpdateTime)
        additional_metadata = {
            k: v
            for k, v in metadata_data.items()
            if k not in ("$model", "$lastUpdateTime")
        }
        metadata = DigitalTwinMetadata(model=model_str, metadata=additional_metadata)

        # Extract known fields
        contents = {
            k: v
            for k, v in data.items()
            if k not in ("$dtId", "$metadata", "$etag", "$lastUpdateTime")
        }

        return cls(
            dtId=data.get("$dtId", ""),
            metadata=metadata,
            etag=data.get("$etag"),
            lastUpdateTime=metadata_data.get("$lastUpdateTime"),
            contents=contents,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary with $ prefixed keys."""
        metadata_dict = {"$model": self.metadata.model}
        # Add additional metadata properties
        metadata_dict.update(self.metadata.metadata)

        result: Dict[str, Any] = {
            "$dtId": self.dtId,
            "$metadata": metadata_dict,
        }
        if self.etag is not None:
            result["$etag"] = self.etag
        if self.lastUpdateTime is not None:
            result["$metadata"]["$lastUpdateTime"] = self.lastUpdateTime
        result.update(self.contents)
        return result


@dataclass
class BasicRelationship:
    """
    A structured relationship following the Azure Digital Twins BasicRelationship pattern.

    This class provides proper typing and validation for relationship data,
    making it compatible with MCP schema generation for LLMs.

    Attributes:
        relationshipId: The unique ID of the relationship.
        sourceId: The ID of the source digital twin.
        targetId: The ID of the target digital twin.
        relationshipName: The name/type of the relationship (e.g., "contains", "isPartOf").
        etag: Optional ETag for concurrency control.
        properties: Additional custom properties defined in the DTDL model.
    """

    relationshipId: RelationshipId  # Represents $relationshipId in JSON
    sourceId: DigitalTwinId  # Represents $sourceId in JSON
    targetId: DigitalTwinId  # Represents $targetId in JSON
    relationshipName: RelationshipName  # Represents $relationshipName in JSON
    etag: Optional[str] = None  # Represents $etag in JSON
    properties: Dict[str, Any] = field(
        default_factory=dict
    )  # Custom relationship properties

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BasicRelationship":
        """Create a BasicRelationship from a dictionary with $ prefixed keys."""
        # Extract known fields
        properties = {
            k: v
            for k, v in data.items()
            if k
            not in (
                "$relationshipId",
                "$sourceId",
                "$targetId",
                "$relationshipName",
                "$etag",
            )
        }

        return cls(
            relationshipId=data.get("$relationshipId", ""),
            sourceId=data.get("$sourceId", ""),
            targetId=data.get("$targetId", ""),
            relationshipName=data.get("$relationshipName", ""),
            etag=data.get("$etag"),
            properties=properties,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary with $ prefixed keys."""
        result: Dict[str, Any] = {
            "$relationshipId": self.relationshipId,
            "$sourceId": self.sourceId,
            "$targetId": self.targetId,
            "$relationshipName": self.relationshipName,
        }
        if self.etag is not None:
            result["$etag"] = self.etag
        result.update(self.properties)
        return result


@dataclass
class BasicDigitalTwinComponent:
    """
    A component within a digital twin.

    Components are nested objects within a digital twin that have their own metadata.

    Attributes:
        metadata: Metadata about the component.
        properties: Component properties defined in the DTDL model.
    """

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )  # Represents $metadata in JSON
    properties: Dict[str, Any] = field(
        default_factory=dict
    )  # Custom component properties

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BasicDigitalTwinComponent":
        """Create a BasicDigitalTwinComponent from a dictionary."""
        properties = {k: v for k, v in data.items() if k != "$metadata"}
        return cls(metadata=data.get("$metadata", {}), properties=properties)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary with $ prefixed keys."""
        result = {"$metadata": self.metadata}
        result.update(self.properties)
        return result


# ============================================================================
# DTDL (Digital Twins Definition Language) Model Types - v3 & v4
# ============================================================================

# Localizable string support
DtdlLocalizableString = Union[str, Dict[str, str]]  # string or {countryCode: string}

# Primitive schema types
DtdlPrimitiveSchema = Literal[
    "boolean",
    "date",
    "dateTime",
    "double",
    "duration",
    "float",
    "integer",
    "long",
    "string",
    "time",
]


@dataclass
class DtdlEnumValue:
    """A value in a DTDL enum schema."""

    name: str
    enumValue: Union[str, int]
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None
    comment: Optional[str] = None
    id: Optional[str] = None  # Represents @id in JSON

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlEnumValue":
        return cls(
            name=data["name"],
            enumValue=data["enumValue"],
            displayName=data.get("displayName"),
            description=data.get("description"),
            comment=data.get("comment"),
            id=data.get("@id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "enumValue": self.enumValue,
        }
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        if self.comment is not None:
            result["comment"] = self.comment
        if self.id is not None:
            result["@id"] = self.id
        return result


@dataclass
class DtdlEnumSchema:
    """A DTDL enum schema definition."""

    type: Literal["Enum"]  # Represents @type in JSON
    enumValues: List[DtdlEnumValue]
    valueSchema: Literal["integer", "string"]
    id: Optional[str] = None  # Represents @id in JSON
    comment: Optional[str] = None
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlEnumSchema":
        return cls(
            type="Enum",
            enumValues=[DtdlEnumValue.from_dict(v) for v in data.get("enumValues", [])],
            valueSchema=data.get("valueSchema", "string"),
            id=data.get("@id"),
            comment=data.get("comment"),
            displayName=data.get("displayName"),
            description=data.get("description"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "@type": self.type,
            "enumValues": [v.to_dict() for v in self.enumValues],
            "valueSchema": self.valueSchema,
        }
        if self.id is not None:
            result["@id"] = self.id
        if self.comment is not None:
            result["comment"] = self.comment
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        return result


@dataclass
class DtdlMapKey:
    """Key definition for a DTDL map schema."""

    name: str
    schema: Literal["string"]
    id: Optional[str] = None  # Represents @id in JSON
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None
    comment: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlMapKey":
        return cls(
            name=data["name"],
            schema="string",
            id=data.get("@id"),
            displayName=data.get("displayName"),
            description=data.get("description"),
            comment=data.get("comment"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"name": self.name, "schema": self.schema}
        if self.id is not None:
            result["@id"] = self.id
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        if self.comment is not None:
            result["comment"] = self.comment
        return result


@dataclass
class DtdlMapValue:
    """Value definition for a DTDL map schema."""

    name: str
    schema: Union[str, Dict[str, Any]]  # Can be primitive string or complex schema
    id: Optional[str] = None  # Represents @id in JSON
    comment: Optional[str] = None
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlMapValue":
        return cls(
            name=data["name"],
            schema=data["schema"],
            id=data.get("@id"),
            comment=data.get("comment"),
            displayName=data.get("displayName"),
            description=data.get("description"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"name": self.name, "schema": self.schema}
        if self.id is not None:
            result["@id"] = self.id
        if self.comment is not None:
            result["comment"] = self.comment
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        return result


@dataclass
class DtdlMapSchema:
    """A DTDL map schema definition."""

    type: Literal["Map"]  # Represents @type in JSON
    mapKey: DtdlMapKey
    mapValue: DtdlMapValue
    id: Optional[str] = None  # Represents @id in JSON
    comment: Optional[str] = None
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlMapSchema":
        return cls(
            type="Map",
            mapKey=DtdlMapKey.from_dict(data["mapKey"]),
            mapValue=DtdlMapValue.from_dict(data["mapValue"]),
            id=data.get("@id"),
            comment=data.get("comment"),
            displayName=data.get("displayName"),
            description=data.get("description"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "@type": self.type,
            "mapKey": self.mapKey.to_dict(),
            "mapValue": self.mapValue.to_dict(),
        }
        if self.id is not None:
            result["@id"] = self.id
        if self.comment is not None:
            result["comment"] = self.comment
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        return result


@dataclass
class DtdlObjectField:
    """A field in a DTDL object schema."""

    name: str
    schema: Union[str, Dict[str, Any]]  # Can be primitive string or complex schema
    id: Optional[str] = None  # Represents @id in JSON
    type: Optional[Union[str, List[str]]] = None  # Represents @type in JSON
    comment: Optional[str] = None
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlObjectField":
        return cls(
            name=data["name"],
            schema=data["schema"],
            id=data.get("@id"),
            type=data.get("@type"),
            comment=data.get("comment"),
            displayName=data.get("displayName"),
            description=data.get("description"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"name": self.name, "schema": self.schema}
        if self.id is not None:
            result["@id"] = self.id
        if self.type is not None:
            result["@type"] = self.type
        if self.comment is not None:
            result["comment"] = self.comment
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        return result


@dataclass
class DtdlObjectSchema:
    """A DTDL object schema definition."""

    type: Union[Literal["Object"], List[str]]  # Represents @type in JSON
    fields: List[DtdlObjectField]
    id: Optional[str] = None  # Represents @id in JSON
    comment: Optional[str] = None
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlObjectSchema":
        return cls(
            type=data.get("@type", "Object"),
            fields=[DtdlObjectField.from_dict(f) for f in data.get("fields", [])],
            id=data.get("@id"),
            comment=data.get("comment"),
            displayName=data.get("displayName"),
            description=data.get("description"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "@type": self.type,
            "fields": [f.to_dict() for f in self.fields],
        }
        if self.id is not None:
            result["@id"] = self.id
        if self.comment is not None:
            result["comment"] = self.comment
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        return result


@dataclass
class DtdlArraySchema:
    """A DTDL array schema definition."""

    type: Literal["Array"]  # Represents @type in JSON
    elementSchema: Union[
        str, Dict[str, Any]
    ]  # Can be primitive string or complex schema
    id: Optional[str] = None  # Represents @id in JSON

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlArraySchema":
        return cls(
            type="Array",
            elementSchema=data["elementSchema"],
            id=data.get("@id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "@type": self.type,
            "elementSchema": self.elementSchema,
        }
        if self.id is not None:
            result["@id"] = self.id
        return result


# Complex schema types
DtdlComplexSchema = Union[
    DtdlEnumSchema, DtdlMapSchema, DtdlObjectSchema, DtdlArraySchema
]
DtdlSchema = Union[DtdlComplexSchema, DtdlPrimitiveSchema, Dict[str, Any]]


@dataclass
class DtdlProperty:
    """A DTDL property definition."""

    name: str
    schema: Union[str, Dict[str, Any]]  # Can be primitive string or complex schema
    type: Union[Literal["Property"], List[str]]  # Represents @type in JSON
    id: Optional[str] = None  # Represents @id in JSON
    comment: Optional[str] = None
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None
    unit: Optional[str] = None
    writable: Optional[bool] = None
    overrides: Optional[str] = None  # Overriding extension
    annotates: Optional[str] = None  # Annotation extension

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlProperty":
        return cls(
            name=data["name"],
            schema=data["schema"],
            type=data.get("@type", "Property"),
            id=data.get("@id"),
            comment=data.get("comment"),
            displayName=data.get("displayName"),
            description=data.get("description"),
            unit=data.get("unit"),
            writable=data.get("writable"),
            overrides=data.get("overrides"),
            annotates=data.get("annotates"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "schema": self.schema,
            "@type": self.type,
        }
        if self.id is not None:
            result["@id"] = self.id
        if self.comment is not None:
            result["comment"] = self.comment
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        if self.unit is not None:
            result["unit"] = self.unit
        if self.writable is not None:
            result["writable"] = self.writable
        if self.overrides is not None:
            result["overrides"] = self.overrides
        if self.annotates is not None:
            result["annotates"] = self.annotates
        return result


@dataclass
class DtdlRelationship:
    """A DTDL relationship definition."""

    name: str
    type: Literal["Relationship"]  # Represents @type in JSON
    target: str
    properties: List[DtdlProperty]
    id: Optional[str] = None  # Represents @id in JSON
    comment: Optional[str] = None
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlRelationship":
        return cls(
            name=data["name"],
            type="Relationship",
            target=data["target"],
            properties=[DtdlProperty.from_dict(p) for p in data.get("properties", [])],
            id=data.get("@id"),
            comment=data.get("comment"),
            displayName=data.get("displayName"),
            description=data.get("description"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "@type": self.type,
            "target": self.target,
            "properties": [p.to_dict() for p in self.properties],
        }
        if self.id is not None:
            result["@id"] = self.id
        if self.comment is not None:
            result["comment"] = self.comment
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        return result


@dataclass
class DtdlTelemetry:
    """A DTDL telemetry definition."""

    name: str
    schema: Union[str, Dict[str, Any]]  # Can be primitive string or complex schema
    type: Union[Literal["Telemetry"], List[str]]  # Represents @type in JSON
    id: Optional[str] = None  # Represents @id in JSON
    comment: Optional[str] = None
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None
    unit: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlTelemetry":
        return cls(
            name=data["name"],
            schema=data["schema"],
            type=data.get("@type", "Telemetry"),
            id=data.get("@id"),
            comment=data.get("comment"),
            displayName=data.get("displayName"),
            description=data.get("description"),
            unit=data.get("unit"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "schema": self.schema,
            "@type": self.type,
        }
        if self.id is not None:
            result["@id"] = self.id
        if self.comment is not None:
            result["comment"] = self.comment
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        if self.unit is not None:
            result["unit"] = self.unit
        return result


@dataclass
class DtdlComponent:
    """A DTDL component definition."""

    name: str
    schema: str  # Reference to another Interface
    type: Literal["Component"]  # Represents @type in JSON
    id: Optional[str] = None  # Represents @id in JSON
    comment: Optional[str] = None
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlComponent":
        return cls(
            name=data["name"],
            schema=data["schema"],
            type="Component",
            id=data.get("@id"),
            comment=data.get("comment"),
            displayName=data.get("displayName"),
            description=data.get("description"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "schema": self.schema,
            "@type": self.type,
        }
        if self.id is not None:
            result["@id"] = self.id
        if self.comment is not None:
            result["comment"] = self.comment
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        return result


@dataclass
class DtdlCommand:
    """A DTDL command definition."""

    name: str
    type: Union[Literal["Command"], List[str]]  # Represents @type in JSON
    request: Optional[Dict[str, Any]] = None  # Request schema
    response: Optional[Dict[str, Any]] = None  # Response schema
    id: Optional[str] = None  # Represents @id in JSON
    comment: Optional[str] = None
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlCommand":
        return cls(
            name=data["name"],
            request=data.get("request"),
            response=data.get("response"),
            type=data.get("@type", "Command"),
            id=data.get("@id"),
            comment=data.get("comment"),
            displayName=data.get("displayName"),
            description=data.get("description"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "@type": self.type,
        }
        if self.request is not None:
            result["request"] = self.request
        if self.response is not None:
            result["response"] = self.response
        if self.id is not None:
            result["@id"] = self.id
        if self.comment is not None:
            result["comment"] = self.comment
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        return result


# Content can be any of these types
DtdlContent = Union[
    DtdlProperty,
    DtdlRelationship,
    DtdlTelemetry,
    DtdlComponent,
    DtdlCommand,
    Dict[str, Any],
]


@dataclass
class DtdlInterface:
    """
    A DTDL Interface definition (v3 & v4).

    This represents a complete Digital Twins model definition.
    """

    id: str  # Represents @id in JSON (e.g., "dtmi:com:example:Room;1")
    type: Union[Literal["Interface"], List[str]]  # Represents @type in JSON
    context: Optional[Union[str, List[str]]] = None  # Represents @context in JSON
    contents: Optional[List[Dict[str, Any]]] = (
        None  # Property, Relationship, Telemetry, Component
    )
    comment: Optional[str] = None
    displayName: Optional[DtdlLocalizableString] = None
    description: Optional[DtdlLocalizableString] = None
    extends: Optional[Union[str, List[str]]] = None
    # MQTT extension properties
    telemetryTopic: Optional[str] = None
    commandTopic: Optional[str] = None
    payloadFormat: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DtdlInterface":
        return cls(
            id=data["@id"],
            type=data.get("@type", "Interface"),
            context=data.get("@context"),
            contents=data.get("contents"),
            comment=data.get("comment"),
            displayName=data.get("displayName"),
            description=data.get("description"),
            extends=data.get("extends"),
            telemetryTopic=data.get("telemetryTopic"),
            commandTopic=data.get("commandTopic"),
            payloadFormat=data.get("payloadFormat"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "@id": self.id,
            "@type": self.type,
        }
        if self.context is not None:
            result["@context"] = self.context
        if self.contents is not None:
            result["contents"] = self.contents
        if self.comment is not None:
            result["comment"] = self.comment
        if self.displayName is not None:
            result["displayName"] = self.displayName
        if self.description is not None:
            result["description"] = self.description
        if self.extends is not None:
            result["extends"] = self.extends
        if self.telemetryTopic is not None:
            result["telemetryTopic"] = self.telemetryTopic
        if self.commandTopic is not None:
            result["commandTopic"] = self.commandTopic
        if self.payloadFormat is not None:
            result["payloadFormat"] = self.payloadFormat
        return result


# Telemetry payload
TelemetryPayload = Dict[str, Any]


# Error structure
class ErrorDict(TypedDict, total=False):
    """TypedDict representing an error response."""

    code: str
    message: str
    target: str
    details: List["ErrorDict"]
    innererror: "ErrorDict"
