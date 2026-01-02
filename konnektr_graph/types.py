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
# Type Aliases - for backward compatibility and less strict typing
# ============================================================================

# Model definition structure
ModelDict = Dict[
    str, Any
]  # Contains: @id, @type, @context, displayName, contents, etc.


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


# Import/Delete Job structures
class ImportJobDict(TypedDict, total=False):
    """TypedDict representing an import job."""

    id: str
    status: JobStatus
    inputBlobUri: str
    outputBlobUri: str
    createdDateTime: str
    lastActionDateTime: str
    finishedDateTime: str
    purgeDateTime: str
    error: ErrorDict


class DeleteJobDict(TypedDict, total=False):
    """TypedDict representing a delete job."""

    id: str
    status: JobStatus
    createdDateTime: str
    lastActionDateTime: str
    finishedDateTime: str
    purgeDateTime: str
    error: ErrorDict


# Query result
class QueryResult(TypedDict):
    """TypedDict representing a query result item."""

    # Query results can contain any JSON-serializable data
    pass


# Paged response
class PagedResponse(TypedDict, total=False):
    """TypedDict representing a paged API response."""

    value: List[Any]
    nextLink: str
    continuationToken: str


# Model data response (matches DigitalTwinsModelData from C#)
class ModelDataDict(TypedDict, total=False):
    """TypedDict representing model metadata and definition."""

    id: str
    description: str
    displayName: str
    decommissioned: bool
    uploadTime: str
    model: ModelDict


# Incoming relationship response
class IncomingRelationshipDict(TypedDict):
    """TypedDict representing an incoming relationship."""

    relationshipId: str
    sourceId: str
    relationshipName: str
    relationshipLink: str
