# konnektr_graph/models.py
"""
Konnektr Graph SDK models (Azure-free).
"""
import math
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .exceptions import ValidationError
from .types import (
    DtdlCommand,
    DtdlComponent,
    DtdlInterface,
    DtdlProperty,
    DtdlRelationship,
    DtdlTelemetry,
    ErrorDict,
    JobId,
    JobStatus,
    ModelId,
)


@dataclass
class ImportJob:
    """
    Represents an import job.

    Attributes:
        id: The unique identifier for the job.
        status: The current status of the job (e.g., 'notstarted', 'running', 'completed').
        input_blob_uri: The URI of the input blob.
        output_blob_uri: The URI of the output blob.
        created_date_time: The date and time the job was created (ISO 8601 format).
        last_action_date_time: The date and time of the last action (ISO 8601 format).
        finished_date_time: The date and time the job finished (ISO 8601 format).
        purge_date_time: The date and time the job will be purged (ISO 8601 format).
        error: Optional error information if the job failed.
    """

    id: JobId
    status: JobStatus
    input_blob_uri: str
    output_blob_uri: str
    created_date_time: str
    last_action_date_time: Optional[str] = None
    finished_date_time: Optional[str] = None
    purge_date_time: Optional[str] = None
    error: Optional[ErrorDict] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ImportJob":
        """
        Create an ImportJob instance from a dictionary.

        Args:
            data: A dictionary containing the import job data.

        Returns:
            An ImportJob instance.
        """
        return cls(
            id=data.get("id", ""),
            status=data.get("status", "notstarted"),
            input_blob_uri=data.get("inputBlobUri", ""),
            output_blob_uri=data.get("outputBlobUri", ""),
            created_date_time=data.get("createdDateTime", ""),
            last_action_date_time=data.get("lastActionDateTime"),
            finished_date_time=data.get("finishedDateTime"),
            purge_date_time=data.get("purgeDateTime"),
            error=data.get("error"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the ImportJob instance to a dictionary.

        Returns:
            A dictionary representation of the ImportJob.
        """
        result: Dict[str, Any] = {
            "id": self.id,
            "status": self.status,
            "inputBlobUri": self.input_blob_uri,
            "outputBlobUri": self.output_blob_uri,
            "createdDateTime": self.created_date_time,
        }
        if self.last_action_date_time is not None:
            result["lastActionDateTime"] = self.last_action_date_time
        if self.finished_date_time is not None:
            result["finishedDateTime"] = self.finished_date_time
        if self.purge_date_time is not None:
            result["purgeDateTime"] = self.purge_date_time
        if self.error is not None:
            result["error"] = self.error
        return result


@dataclass
class DeleteJob:
    """
    Represents a delete job.

    Attributes:
        id: The unique identifier for the job.
        status: The current status of the job (e.g., 'notstarted', 'running', 'completed').
        created_date_time: The date and time the job was created (ISO 8601 format).
        last_action_date_time: The date and time of the last action (ISO 8601 format).
        finished_date_time: The date and time the job finished (ISO 8601 format).
        purge_date_time: The date and time the job will be purged (ISO 8601 format).
        error: Optional error information if the job failed.
    """

    id: JobId
    status: JobStatus
    created_date_time: str
    last_action_date_time: Optional[str] = None
    finished_date_time: Optional[str] = None
    purge_date_time: Optional[str] = None
    error: Optional[ErrorDict] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeleteJob":
        """
        Create a DeleteJob instance from a dictionary.

        Args:
            data: A dictionary containing the delete job data.

        Returns:
            A DeleteJob instance.
        """
        return cls(
            id=data.get("id", ""),
            status=data.get("status", "notstarted"),
            created_date_time=data.get("createdDateTime", ""),
            last_action_date_time=data.get("lastActionDateTime"),
            finished_date_time=data.get("finishedDateTime"),
            purge_date_time=data.get("purgeDateTime"),
            error=data.get("error"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the DeleteJob instance to a dictionary.

        Returns:
            A dictionary representation of the DeleteJob.
        """
        result: Dict[str, Any] = {
            "id": self.id,
            "status": self.status,
            "createdDateTime": self.created_date_time,
        }
        if self.last_action_date_time is not None:
            result["lastActionDateTime"] = self.last_action_date_time
        if self.finished_date_time is not None:
            result["finishedDateTime"] = self.finished_date_time
        if self.purge_date_time is not None:
            result["purgeDateTime"] = self.purge_date_time
        if self.error is not None:
            result["error"] = self.error
        return result


@dataclass
class DigitalTwinsModelData:
    """
    Represents a DTDL model metadata and definition.

    Attributes:
        id: The unique identifier for the model.
        description: Optional description of the model.
        display_name: Optional display name of the model.
        decommissioned: Whether the model is decommissioned.
        upload_time: The date and time the model was uploaded (ISO 8601 format).
        model: The full DTDL model definition.
    """

    id: ModelId
    description: Optional[str] = None
    display_name: Optional[str] = None
    decommissioned: bool = False
    upload_time: Optional[str] = None
    model: Optional[DtdlInterface] = None
    embedding: Optional[List[float]] = None
    bases: Optional[list[str]] = None
    properties: Optional[list[DtdlProperty]] = None
    relationships: Optional[list[DtdlRelationship]] = None
    components: Optional[list[DtdlComponent]] = None
    telemetries: Optional[list[DtdlTelemetry]] = None
    commands: Optional[list[DtdlCommand]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DigitalTwinsModelData":
        """
        Create a DigitalTwinsModelData instance from a dictionary.

        Args:
            data: A dictionary containing the model data.

        Returns:
            A DigitalTwinsModelData instance.
        """
        model_data = data.get("model")
        return cls(
            id=data.get("id", ""),
            description=data.get("description"),
            display_name=data.get("displayName"),
            decommissioned=data.get("decommissioned", False),
            upload_time=data.get("uploadTime"),
            embedding=data.get("embedding"),
            model=(
                DtdlInterface.from_dict(model_data) if model_data is not None else None
            ),
            bases=data.get("bases"),
            properties=(
                [DtdlProperty.from_dict(p) for p in data["properties"] if isinstance(p, dict)]
                if "properties" in data and isinstance(data["properties"], list)
                else None
            ),
            relationships=(
                [DtdlRelationship.from_dict(r) for r in data["relationships"] if isinstance(r, dict)]
                if "relationships" in data and isinstance(data["relationships"], list)
                else None
            ),
            components=(
                [DtdlComponent.from_dict(c) for c in data["components"] if isinstance(c, dict)]
                if "components" in data and isinstance(data["components"], list)
                else None
            ),
            telemetries=(
                [DtdlTelemetry.from_dict(t) for t in data["telemetries"] if isinstance(t, dict)]
                if "telemetries" in data and isinstance(data["telemetries"], list)
                else None
            ),
            commands=(
                [DtdlCommand.from_dict(c) for c in data["commands"] if isinstance(c, dict)]
                if "commands" in data and isinstance(data["commands"], list)
                else None
            ),
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the DigitalTwinsModelData instance to a dictionary.

        Returns:
            A dictionary representation of the DigitalTwinsModelData.
        """
        result: Dict[str, Any] = {
            "id": self.id,
            "decommissioned": self.decommissioned,
        }
        if self.description is not None:
            result["description"] = self.description
        if self.display_name is not None:
            result["displayName"] = self.display_name
        if self.upload_time is not None:
            result["uploadTime"] = self.upload_time
        if self.model is not None:
            result["model"] = self.model.to_dict()
        if self.embedding is not None:
            result["embedding"] = self.embedding
        if self.bases is not None:
            result["bases"] = self.bases
        if self.properties is not None:
            result["properties"] = [p.to_dict() for p in self.properties]
        if self.relationships is not None:
            result["relationships"] = [r.to_dict() for r in self.relationships]
        if self.components is not None:
            result["components"] = [c.to_dict() for c in self.components]
        if self.telemetries is not None:
            result["telemetries"] = [t.to_dict() for t in self.telemetries]
        if self.commands is not None:
            result["commands"] = [c.to_dict() for c in self.commands]
        return result


# --- Scoped vector memory search ---
#
# Typed client surface for POST /digitaltwins/memory-search (+ the companion
# /digitaltwins/memory-search/index and .../capability endpoints). The wire
# shape mirrors the graph API: camelCase field names, null optionals omitted.

#: Maximum number of ranked records a single memory search may request (1..100).
MEMORY_SEARCH_MAX_LIMIT = 100

#: Maximum supported query-vector dimensionality (HNSW index limit).
MEMORY_SEARCH_MAX_VECTOR_DIMENSIONS = 2000

#: Maximum excerpt characters per memory-search record (1..4000).
MEMORY_SEARCH_MAX_EXCERPT_LENGTH = 4000

_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _check_embedding_property(embedding_property: str) -> None:
    if not embedding_property or not _IDENTIFIER_PATTERN.match(embedding_property):
        raise ValidationError(
            f"Embedding property '{embedding_property}' is not a valid property identifier."
        )


def validate_memory_search_options(
    vector: List[float],
    embedding_property: str = "embedding",
    limit: int = 10,
    model_ids: Optional[List[str]] = None,
    property_filters: Optional[Dict[str, str]] = None,
    related_twin_id: Optional[str] = None,
    expected_dimension: Optional[int] = None,
    excerpt_length: Optional[int] = None,
) -> None:
    """Validate scoped memory-search arguments client-side.

    Mirrors the server bounds; server validation remains authoritative.

    Raises:
        ValidationError: If any argument violates its constraint.
    """
    if not vector:
        raise ValidationError("Query vector must contain at least one dimension.")
    if len(vector) > MEMORY_SEARCH_MAX_VECTOR_DIMENSIONS:
        raise ValidationError(
            f"Query vector has {len(vector)} dimensions, which exceeds the maximum "
            f"of {MEMORY_SEARCH_MAX_VECTOR_DIMENSIONS}."
        )
    if any(not isinstance(v, (int, float)) or not math.isfinite(v) for v in vector):
        raise ValidationError("Query vector must only contain finite numbers.")
    _check_embedding_property(embedding_property)
    if limit < 1 or limit > MEMORY_SEARCH_MAX_LIMIT:
        raise ValidationError(f"Limit must be between 1 and {MEMORY_SEARCH_MAX_LIMIT}.")
    if model_ids is not None:
        for model_id in model_ids:
            if not model_id or not model_id.strip():
                raise ValidationError("Model allow-list must not contain empty model IDs.")
    if property_filters is not None:
        for key, value in property_filters.items():
            if not key or not _IDENTIFIER_PATTERN.match(key):
                raise ValidationError(
                    f"Property filter key '{key}' is not a valid property identifier."
                )
            if value is None:
                raise ValidationError(
                    f"Property filter '{key}' must have a non-null value."
                )
    if related_twin_id is not None and not related_twin_id.strip():
        raise ValidationError("Related twin ID must not be empty when provided.")
    if expected_dimension is not None:
        if (
            expected_dimension < 1
            or expected_dimension > MEMORY_SEARCH_MAX_VECTOR_DIMENSIONS
        ):
            raise ValidationError(
                "Expected dimension must be between 1 and "
                f"{MEMORY_SEARCH_MAX_VECTOR_DIMENSIONS}."
            )
        if expected_dimension != len(vector):
            raise ValidationError(
                f"Query vector has {len(vector)} dimensions but "
                f"{expected_dimension} were expected."
            )
    if excerpt_length is not None and (
        excerpt_length < 1 or excerpt_length > MEMORY_SEARCH_MAX_EXCERPT_LENGTH
    ):
        raise ValidationError(
            "Excerpt length must be between 1 and "
            f"{MEMORY_SEARCH_MAX_EXCERPT_LENGTH}."
        )


def validate_memory_search_index_options(
    dimension: int,
    embedding_property: str = "embedding",
    m: Optional[int] = None,
    ef_construction: Optional[int] = None,
) -> None:
    """Validate memory-search HNSW index arguments client-side.

    Raises:
        ValidationError: If any argument violates its constraint.
    """
    _check_embedding_property(embedding_property)
    if dimension < 1 or dimension > MEMORY_SEARCH_MAX_VECTOR_DIMENSIONS:
        raise ValidationError(
            "Index dimension must be between 1 and "
            f"{MEMORY_SEARCH_MAX_VECTOR_DIMENSIONS}."
        )
    if m is not None and (m < 2 or m > 100):
        raise ValidationError("HNSW m must be between 2 and 100.")
    if ef_construction is not None and (ef_construction < 4 or ef_construction > 1000):
        raise ValidationError("HNSW ef_construction must be between 4 and 1000.")


@dataclass
class MemorySearchResult:
    """
    A single ranked record from scoped vector memory search.

    Scope predicates (model allow-list, property equality filters, related-twin
    predicate) are applied by the server in the database *before*
    nearest-neighbour ranking and ``LIMIT`` — the ranking never sees
    out-of-scope records.

    Attributes:
        id: Stable twin ID ($dtId).
        model_id: Twin model ID ($metadata.$model), when known.
        distance: L2 distance to the query vector. Lower values rank first.
        excerpt: Bounded JSON excerpt of the twin's properties. The embedding
            vector itself is excluded; fetch the full twin via
            ``get_digital_twin`` when needed.
        last_updated_on: Last update time of the twin, when known (ISO 8601).
    """

    id: str
    distance: float
    excerpt: str
    model_id: Optional[str] = None
    last_updated_on: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemorySearchResult":
        """
        Create a MemorySearchResult instance from a dictionary.

        Args:
            data: A dictionary containing the memory search result data
                (camelCase wire shape).

        Returns:
            A MemorySearchResult instance.
        """
        return cls(
            id=data.get("id", ""),
            distance=data.get("distance", 0.0),
            excerpt=data.get("excerpt", ""),
            model_id=data.get("modelId"),
            last_updated_on=data.get("lastUpdatedOn"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the MemorySearchResult instance to a dictionary.

        Returns:
            A dictionary representation of the MemorySearchResult (camelCase).
        """
        result: Dict[str, Any] = {
            "id": self.id,
            "distance": self.distance,
            "excerpt": self.excerpt,
        }
        if self.model_id is not None:
            result["modelId"] = self.model_id
        if self.last_updated_on is not None:
            result["lastUpdatedOn"] = self.last_updated_on
        return result


@dataclass
class MemorySearchCapability:
    """
    Capability report for scoped vector memory search.

    Attributes:
        vector_search_available: True when the pgvector extension is installed
            and memory search can be served.
    """

    vector_search_available: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemorySearchCapability":
        """
        Create a MemorySearchCapability instance from a dictionary.

        Args:
            data: A dictionary containing the capability data (camelCase wire shape).

        Returns:
            A MemorySearchCapability instance.
        """
        return cls(vector_search_available=data.get("vectorSearchAvailable", False))

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the MemorySearchCapability instance to a dictionary.

        Returns:
            A dictionary representation of the MemorySearchCapability (camelCase).
        """
        return {"vectorSearchAvailable": self.vector_search_available}


@dataclass
class MemorySearchIndex:
    """
    The HNSW index backing scoped vector memory search.

    Attributes:
        index_name: Name of the index (pre-existing when already created).
        dimension: Embedding dimensionality the index was built for.
    """

    index_name: str
    dimension: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemorySearchIndex":
        """
        Create a MemorySearchIndex instance from a dictionary.

        Args:
            data: A dictionary containing the index data (camelCase wire shape).

        Returns:
            A MemorySearchIndex instance.
        """
        return cls(
            index_name=data.get("indexName", ""),
            dimension=data.get("dimension", 0),
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the MemorySearchIndex instance to a dictionary.

        Returns:
            A dictionary representation of the MemorySearchIndex (camelCase).
        """
        return {"indexName": self.index_name, "dimension": self.dimension}
