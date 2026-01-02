# konnektr_graph/models.py
"""
Konnektr Graph SDK models (Azure-free).
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .types import (
    DtdlInterface,
    ErrorDict,
    JobId,
    JobStatus,
    ModelId,
    RelationshipId,
    RelationshipName,
    DigitalTwinId,
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
            id=data["id"],
            status=data["status"],
            input_blob_uri=data["inputBlobUri"],
            output_blob_uri=data["outputBlobUri"],
            created_date_time=data["createdDateTime"],
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
            id=data["id"],
            status=data["status"],
            created_date_time=data["createdDateTime"],
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
            id=data["id"],
            description=data.get("description"),
            display_name=data.get("displayName"),
            decommissioned=data.get("decommissioned", False),
            upload_time=data.get("uploadTime"),
            model=(
                DtdlInterface.from_dict(model_data) if model_data is not None else None
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
            result["model"] = (
                self.model.to_dict() if hasattr(self.model, "to_dict") else self.model
            )
        return result
