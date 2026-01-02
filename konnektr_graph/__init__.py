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
)
from .types import (
    # Structured Models (Dataclasses)
    BasicDigitalTwin,
    BasicRelationship,
    BasicDigitalTwinComponent,
    DigitalTwinMetadata,
    # DTDL Model Types
    DtdlInterface,
    DtdlProperty,
    DtdlRelationship,
    DtdlTelemetry,
    DtdlComponent,
    DtdlEnumSchema,
    DtdlMapSchema,
    DtdlObjectSchema,
    DtdlArraySchema,
    DtdlObjectField,
    DtdlEnumValue,
    DtdlMapKey,
    DtdlMapValue,
    DtdlLocalizableString,
    DtdlPrimitiveSchema,
    DtdlSchema,
    DtdlContent,
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
    JsonPatchOperation,
    TelemetryPayload,
    ErrorDict,
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
    # Structured Models (Dataclasses)
    "BasicDigitalTwin",
    "BasicRelationship",
    "BasicDigitalTwinComponent",
    "DigitalTwinMetadata",
    # DTDL Model Types
    "DtdlInterface",
    "DtdlProperty",
    "DtdlRelationship",
    "DtdlTelemetry",
    "DtdlComponent",
    "DtdlEnumSchema",
    "DtdlMapSchema",
    "DtdlObjectSchema",
    "DtdlArraySchema",
    "DtdlObjectField",
    "DtdlEnumValue",
    "DtdlMapKey",
    "DtdlMapValue",
    "DtdlLocalizableString",
    "DtdlPrimitiveSchema",
    "DtdlSchema",
    "DtdlContent",
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
    "JsonPatchOperation",
    "TelemetryPayload",
    "ErrorDict",
]
