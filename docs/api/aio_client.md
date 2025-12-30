<a id="konnektr_graph.aio.client"></a>

# konnektr\_graph.aio.client

Konnektr Graph SDK (Azure-free) - Asynchronous Client

<a id="konnektr_graph.aio.client.AsyncPagedIterator"></a>

## AsyncPagedIterator Objects

```python
class AsyncPagedIterator(AsyncIterator)
```

Async iterator for handling paged responses.
Supports both nextLink in body and x-ms-continuation in headers.

<a id="konnektr_graph.aio.client.AsyncPagedIterator.__init__"></a>

#### \_\_init\_\_

```python
def __init__(client: "KonnektrGraphClient",
             initial_url: str,
             method: str = "GET",
             headers: Optional[Dict[str, str]] = None,
             json_data: Optional[Dict[str, Any]] = None,
             params: Optional[Dict[str, Any]] = None,
             model_cls: Any = None,
             items_key: str = "value")
```

Initialize the async paged iterator.

**Arguments**:

- `client` - The KonnektrGraphClient instance.
- `initial_url` - The initial URL for the first page.
- `method` - The HTTP method to use. Defaults to "GET".
- `headers` - Optional headers to include in the request.
- `json_data` - Optional JSON body for the request.
- `params` - Optional query parameters for the request.
- `model_cls` - Optional class to instantiate for each item in the results.
- `items_key` - The key in the JSON response that contains the items list. Defaults to "value".

<a id="konnektr_graph.aio.client.KonnektrGraphClient"></a>

## KonnektrGraphClient Objects

```python
class KonnektrGraphClient()
```

<a id="konnektr_graph.aio.client.KonnektrGraphClient.__init__"></a>

#### \_\_init\_\_

```python
def __init__(endpoint: str, credential: Union[AsyncTokenProvider,
                                              TokenProvider])
```

Initialize the Konnektr Graph Client.

**Arguments**:

- `endpoint` - API endpoint (e.g. https://graph.konnektr.io)
- `credential` - AsyncTokenProvider or TokenProvider credential for authentication.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.close"></a>

#### close

```python
async def close()
```

Close the client session.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.get_digital_twin"></a>

#### get\_digital\_twin

```python
async def get_digital_twin(digital_twin_id: str,
                           **kwargs: Any) -> Dict[str, Any]
```

Get a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `**kwargs` - Additional request options.
  

**Returns**:

  The digital twin data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.upsert_digital_twin"></a>

#### upsert\_digital\_twin

```python
async def upsert_digital_twin(digital_twin_id: str, digital_twin: Dict[str,
                                                                       Any],
                              **kwargs: Any) -> Dict[str, Any]
```

Create or update a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `digital_twin` - The digital twin data to create or update.
- `**kwargs` - Additional request options.
  

**Returns**:

  The created or updated digital twin data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.update_digital_twin"></a>

#### update\_digital\_twin

```python
async def update_digital_twin(digital_twin_id: str,
                              json_patch: List[Dict[str, Any]],
                              **kwargs: Any) -> None
```

Update a digital twin (JSON Patch).

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `json_patch` - The JSON patch to apply.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.delete_digital_twin"></a>

#### delete\_digital\_twin

```python
async def delete_digital_twin(digital_twin_id: str, **kwargs: Any) -> None
```

Delete a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.get_component"></a>

#### get\_component

```python
async def get_component(digital_twin_id: str, component_name: str,
                        **kwargs: Any) -> Dict[str, Any]
```

Get a component.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `component_name` - The name of the component.
- `**kwargs` - Additional request options.
  

**Returns**:

  The component data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.update_component"></a>

#### update\_component

```python
async def update_component(digital_twin_id: str, component_name: str,
                           json_patch: List[Dict[str,
                                                 Any]], **kwargs: Any) -> None
```

Update a component.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `component_name` - The name of the component.
- `json_patch` - The JSON patch to apply.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.get_relationship"></a>

#### get\_relationship

```python
async def get_relationship(digital_twin_id: str, relationship_id: str,
                           **kwargs: Any) -> Dict[str, Any]
```

Get a relationship.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `relationship_id` - The ID of the relationship.
- `**kwargs` - Additional request options.
  

**Returns**:

  The relationship data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.upsert_relationship"></a>

#### upsert\_relationship

```python
async def upsert_relationship(digital_twin_id: str, relationship_id: str,
                              relationship: Dict[str, Any],
                              **kwargs: Any) -> Dict[str, Any]
```

Create or update a relationship.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `relationship_id` - The ID of the relationship.
- `relationship` - The relationship data.
- `**kwargs` - Additional request options.
  

**Returns**:

  The created or updated relationship data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.update_relationship"></a>

#### update\_relationship

```python
async def update_relationship(digital_twin_id: str, relationship_id: str,
                              json_patch: List[Dict[str, Any]],
                              **kwargs: Any) -> None
```

Update a relationship.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `relationship_id` - The ID of the relationship.
- `json_patch` - The JSON patch to apply.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.delete_relationship"></a>

#### delete\_relationship

```python
async def delete_relationship(digital_twin_id: str, relationship_id: str,
                              **kwargs: Any) -> None
```

Delete a relationship.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `relationship_id` - The ID of the relationship.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.list_relationships"></a>

#### list\_relationships

```python
def list_relationships(digital_twin_id: str,
                       relationship_name: Optional[str] = None,
                       **kwargs: Any) -> AsyncPagedIterator
```

List relationships for a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `relationship_name` - Optional name of the relationship to filter by.
- `**kwargs` - Additional request options.
  

**Returns**:

  An async iterator over the relationships.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.list_incoming_relationships"></a>

#### list\_incoming\_relationships

```python
def list_incoming_relationships(digital_twin_id: str,
                                **kwargs: Any) -> AsyncPagedIterator
```

List incoming relationships for a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `**kwargs` - Additional request options.
  

**Returns**:

  An async iterator over the incoming relationships.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.query_twins"></a>

#### query\_twins

```python
def query_twins(query_expression: str,
                max_items_per_page: Optional[int] = None,
                **kwargs: Any) -> AsyncPagedIterator
```

Query digital twins.

**Arguments**:

- `query_expression` - The query expression.
- `max_items_per_page` - Optional maximum items per page.
- `**kwargs` - Additional request options.
  

**Returns**:

  An async iterator over the query results.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.get_model"></a>

#### get\_model

```python
async def get_model(model_id: str,
                    include_model_definition: bool = False,
                    **kwargs: Any) -> DigitalTwinsModelData
```

Get a model.

**Arguments**:

- `model_id` - The ID of the model.
- `include_model_definition` - Whether to include the model definition.
- `**kwargs` - Additional request options.
  

**Returns**:

  The model data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.list_models"></a>

#### list\_models

```python
def list_models(dependencies_for: Optional[Union[str, List[str]]] = None,
                include_model_definition: bool = False,
                results_per_page: Optional[int] = None,
                **kwargs: Any) -> AsyncPagedIterator
```

List models.

**Arguments**:

- `dependencies_for` - Optional model ID or list of model IDs to get dependencies for.
- `include_model_definition` - Whether to include the model definition.
- `results_per_page` - Optional maximum items per page.
- `**kwargs` - Additional request options.
  

**Returns**:

  An async iterator over the models.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.create_models"></a>

#### create\_models

```python
async def create_models(dtdl_models: List[Dict[str, Any]],
                        **kwargs: Any) -> List[DigitalTwinsModelData]
```

Create models.

**Arguments**:

- `dtdl_models` - A list of DTDL model definitions.
- `**kwargs` - Additional request options.
  

**Returns**:

  A list of created model data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.decommission_model"></a>

#### decommission\_model

```python
async def decommission_model(model_id: str, **kwargs: Any) -> None
```

Decommission a model.

**Arguments**:

- `model_id` - The ID of the model.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.delete_model"></a>

#### delete\_model

```python
async def delete_model(model_id: str, **kwargs: Any) -> None
```

Delete a model.

**Arguments**:

- `model_id` - The ID of the model.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.search_models"></a>

#### search\_models

```python
async def search_models(search_text: str,
                        limit: int = 10,
                        **kwargs: Any) -> List[Dict[str, Any]]
```

Search for DTDL models using semantic and keyword search.

**Arguments**:

- `search_text` - Search query (uses hybrid vector + keyword search).
- `limit` - Maximum number of results to return. Defaults to 10.
- `**kwargs` - Additional request options.
  

**Returns**:

  A list of matching model summaries.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.search_twins"></a>

#### search\_twins

```python
async def search_twins(search_text: str,
                       model_id: Optional[str] = None,
                       limit: int = 10,
                       **kwargs: Any) -> List[Dict[str, Any]]
```

Search for digital twins using semantic and keyword search.

**Arguments**:

- `search_text` - Search query.
- `model_id` - Optional filter by model ID.
- `limit` - Maximum number of results to return. Defaults to 10.
- `**kwargs` - Additional request options.
  

**Returns**:

  A list of matching digital twins.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.publish_telemetry"></a>

#### publish\_telemetry

```python
async def publish_telemetry(digital_twin_id: str,
                            telemetry: Dict[str, Any],
                            message_id: Optional[str] = None,
                            **kwargs: Any) -> None
```

Publish telemetry for a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `telemetry` - The telemetry data.
- `message_id` - Optional unique identifier for the telemetry message.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.publish_component_telemetry"></a>

#### publish\_component\_telemetry

```python
async def publish_component_telemetry(digital_twin_id: str,
                                      component_name: str,
                                      telemetry: Dict[str, Any],
                                      message_id: Optional[str] = None,
                                      **kwargs: Any) -> None
```

Publish telemetry for a component.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `component_name` - The name of the component.
- `telemetry` - The telemetry data.
- `message_id` - Optional unique identifier for the telemetry message.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.list_import_jobs"></a>

#### list\_import\_jobs

```python
def list_import_jobs(**kwargs: Any) -> AsyncPagedIterator
```

List import jobs.

**Arguments**:

- `**kwargs` - Additional request options.
  

**Returns**:

  An async iterator over the import jobs.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.get_import_job"></a>

#### get\_import\_job

```python
async def get_import_job(job_id: str, **kwargs: Any) -> ImportJob
```

Get an import job.

**Arguments**:

- `job_id` - The ID of the job.
- `**kwargs` - Additional request options.
  

**Returns**:

  The import job data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.create_import_job"></a>

#### create\_import\_job

```python
async def create_import_job(job_id: str, import_job: Dict[str, Any],
                            **kwargs: Any) -> ImportJob
```

Create an import job.

**Arguments**:

- `job_id` - The ID of the job.
- `import_job` - The import job data.
- `**kwargs` - Additional request options.
  

**Returns**:

  The created import job data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.delete_import_job"></a>

#### delete\_import\_job

```python
async def delete_import_job(job_id: str, **kwargs: Any) -> None
```

Delete an import job.

**Arguments**:

- `job_id` - The ID of the job.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.cancel_import_job"></a>

#### cancel\_import\_job

```python
async def cancel_import_job(job_id: str, **kwargs: Any) -> ImportJob
```

Cancel an import job.

**Arguments**:

- `job_id` - The ID of the job.
- `**kwargs` - Additional request options.
  

**Returns**:

  The cancelled import job data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.list_delete_jobs"></a>

#### list\_delete\_jobs

```python
def list_delete_jobs(**kwargs: Any) -> AsyncPagedIterator
```

List delete jobs.

**Arguments**:

- `**kwargs` - Additional request options.
  

**Returns**:

  An async iterator over the delete jobs.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.get_delete_job"></a>

#### get\_delete\_job

```python
async def get_delete_job(job_id: str, **kwargs: Any) -> DeleteJob
```

Get a delete job.

**Arguments**:

- `job_id` - The ID of the job.
- `**kwargs` - Additional request options.
  

**Returns**:

  The delete job data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.create_delete_job"></a>

#### create\_delete\_job

```python
async def create_delete_job(job_id: str,
                            delete_job: Optional[Dict[str, Any]] = None,
                            **kwargs: Any) -> DeleteJob
```

Create a delete job.

**Arguments**:

- `job_id` - The ID of the job.
- `delete_job` - Optional delete job options.
- `**kwargs` - Additional request options.
  

**Returns**:

  The created delete job data.

