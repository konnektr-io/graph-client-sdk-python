# konnektr_graph/__init__.py
"""
Konnektr Graph SDK (Azure-free).
"""
from .client import KonnektrGraphClient, PagedIterator
from .exceptions import (
    KonnektrGraphError,
    HttpResponseError,
    ResourceNotFoundError,
    ResourceExistsError,
    AuthenticationError,
    ValidationError,
)
from .models import (
    ImportJob,
    DeleteJob,
    DigitalTwinsModelData,
    IncomingRelationship,
)
from .types import (
    # Structured Models (Dataclasses)
    BasicDigitalTwin,
    BasicRelationship,
    BasicDigitalTwinComponent,
    DigitalTwinMetadata,
    # Type aliases
    DigitalTwinId,
    ComponentName,
    RelationshipId,
    RelationshipName,
    ModelId,
    JobId,
    MessageId,
    JobStatus,
    QueryExpression,
    ETag,
    # TypedDicts and utility types
    ModelDict,
    JsonPatchOperation,
    TelemetryPayload,
    ErrorDict,
    ImportJobDict,
    DeleteJobDict,
    ModelDataDict,
    IncomingRelationshipDict,
)

__all__ = [
    # Client
    "KonnektrGraphClient",
    "PagedIterator",
    # Exceptions
    "KonnektrGraphError",
    "HttpResponseError",
    "ResourceNotFoundError",
    "ResourceExistsError",
    "AuthenticationError",
    "ValidationError",
    # Models
    "ImportJob",
    "DeleteJob",
    "DigitalTwinsModelData",
    "IncomingRelationship",
    # Structured Models (Dataclasses)
    "BasicDigitalTwin",
    "BasicRelationship",
    "BasicDigitalTwinComponent",
    "DigitalTwinMetadata",
    # Type aliases
    "DigitalTwinId",
    "ComponentName",
    "RelationshipId",
    "RelationshipName",
    "ModelId",
    "JobId",
    "MessageId",
    "JobStatus",
    "QueryExpression",
    "ETag",
    # TypedDicts and utility types
    "ModelDict",
    "JsonPatchOperation",
    "TelemetryPayload",
    "ErrorDict",
    "ImportJobDict",
    "DeleteJobDict",
    "ModelDataDict",
    "IncomingRelationshipDict",
]
