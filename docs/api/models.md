<a id="konnektr_graph.models"></a>

# konnektr\_graph.models

Konnektr Graph SDK models (Azure-free).

<a id="konnektr_graph.models.ImportJob"></a>

## ImportJob Objects

```python
@dataclass
class ImportJob()
```

Represents an import job.

**Attributes**:

- `id` - The unique identifier for the job.
- `status` - The current status of the job (e.g., 'notstarted', 'running', 'completed').
- `input_blob_uri` - The URI of the input blob.
- `output_blob_uri` - The URI of the output blob.
- `created_date_time` - The date and time the job was created.
- `last_action_date_time` - The date and time of the last action.
- `finished_date_time` - The date and time the job finished.
- `purge_date_time` - The date and time the job will be purged.
- `error` - Optional error information if the job failed.

<a id="konnektr_graph.models.ImportJob.from_dict"></a>

#### from\_dict

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> "ImportJob"
```

Create an ImportJob instance from a dictionary.

**Arguments**:

- `data` - A dictionary containing the import job data.
  

**Returns**:

  An ImportJob instance.

<a id="konnektr_graph.models.DeleteJob"></a>

## DeleteJob Objects

```python
@dataclass
class DeleteJob()
```

Represents a delete job.

**Attributes**:

- `id` - The unique identifier for the job.
- `status` - The current status of the job (e.g., 'notstarted', 'running', 'completed').
- `created_date_time` - The date and time the job was created.
- `last_action_date_time` - The date and time of the last action.
- `finished_date_time` - The date and time the job finished.
- `purge_date_time` - The date and time the job will be purged.
- `error` - Optional error information if the job failed.

<a id="konnektr_graph.models.DeleteJob.from_dict"></a>

#### from\_dict

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> "DeleteJob"
```

Create a DeleteJob instance from a dictionary.

**Arguments**:

- `data` - A dictionary containing the delete job data.
  

**Returns**:

  A DeleteJob instance.

<a id="konnektr_graph.models.DigitalTwinsModelData"></a>

## DigitalTwinsModelData Objects

```python
@dataclass
class DigitalTwinsModelData()
```

Represents a DTDL model metadata and definition.

**Attributes**:

- `id` - The unique identifier for the model.
- `description` - Optional description of the model.
- `display_name` - Optional display name of the model.
- `decommissioned` - Whether the model is decommissioned.
- `upload_time` - The date and time the model was uploaded.
- `model` - The full DTDL model definition.

<a id="konnektr_graph.models.DigitalTwinsModelData.from_dict"></a>

#### from\_dict

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> "DigitalTwinsModelData"
```

Create a DigitalTwinsModelData instance from a dictionary.

**Arguments**:

- `data` - A dictionary containing the model data.
  

**Returns**:

  A DigitalTwinsModelData instance.

<a id="konnektr_graph.models.IncomingRelationship"></a>

## IncomingRelationship Objects

```python
@dataclass
class IncomingRelationship()
```

Represents an incoming relationship for a digital twin.

**Attributes**:

- `relationship_id` - The ID of the relationship.
- `source_id` - The source of the relationship.
- `relationship_name` - The name of the relationship.
- `relationship_link` - A link to the relationship definition.

<a id="konnektr_graph.models.IncomingRelationship.from_dict"></a>

#### from\_dict

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> "IncomingRelationship"
```

Create an IncomingRelationship instance from a dictionary.

**Arguments**:

- `data` - A dictionary containing the relationship data.
  

**Returns**:

  An IncomingRelationship instance.

