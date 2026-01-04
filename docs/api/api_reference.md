<a id="konnektr_graph"></a>

# konnektr\_graph

Konnektr Graph SDK (Azure-free).

<a id="konnektr_graph.aio.client"></a>

# konnektr\_graph.aio.client

Konnektr Graph SDK (Azure-free) - Asynchronous Client

<a id="konnektr_graph.aio.client.AsyncPagedIterator"></a>

## AsyncPagedIterator Objects

```python
class AsyncPagedIterator(AsyncIterator[T], Generic[T])
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
             model_cls: Optional[Type[T]] = None,
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
async def get_digital_twin(digital_twin_id: DigitalTwinId,
                           **kwargs: Any) -> BasicDigitalTwin
```

Get a digital twin by ID.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `**kwargs` - Additional request parameters.
  

**Returns**:

  The digital twin data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.upsert_digital_twin"></a>

#### upsert\_digital\_twin

```python
async def upsert_digital_twin(digital_twin_id: DigitalTwinId,
                              digital_twin: BasicDigitalTwin,
                              **kwargs: Any) -> BasicDigitalTwin
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
async def update_digital_twin(digital_twin_id: DigitalTwinId,
                              json_patch: List[JsonPatchOperation],
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
async def delete_digital_twin(digital_twin_id: DigitalTwinId,
                              **kwargs: Any) -> None
```

Delete a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.get_component"></a>

#### get\_component

```python
async def get_component(digital_twin_id: DigitalTwinId,
                        component_name: ComponentName,
                        **kwargs: Any) -> BasicDigitalTwinComponent
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
async def update_component(digital_twin_id: DigitalTwinId,
                           component_name: ComponentName,
                           json_patch: List[JsonPatchOperation],
                           **kwargs: Any) -> None
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
async def get_relationship(digital_twin_id: DigitalTwinId,
                           relationship_id: RelationshipId,
                           **kwargs: Any) -> BasicRelationship
```

Get a relationship by ID.

**Arguments**:

- `digital_twin_id` - The ID of the source digital twin.
- `relationship_id` - The ID of the relationship.
- `**kwargs` - Additional request parameters.
  

**Returns**:

  The relationship data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.upsert_relationship"></a>

#### upsert\_relationship

```python
async def upsert_relationship(digital_twin_id: DigitalTwinId,
                              relationship_id: RelationshipId,
                              relationship: BasicRelationship,
                              **kwargs: Any) -> BasicRelationship
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
async def update_relationship(digital_twin_id: DigitalTwinId,
                              relationship_id: RelationshipId,
                              json_patch: List[JsonPatchOperation],
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
async def delete_relationship(digital_twin_id: DigitalTwinId,
                              relationship_id: RelationshipId,
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
def list_relationships(digital_twin_id: DigitalTwinId,
                       relationship_name: Optional[RelationshipName] = None,
                       **kwargs: Any) -> AsyncPagedIterator[BasicRelationship]
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
def list_incoming_relationships(
        digital_twin_id: DigitalTwinId,
        **kwargs: Any) -> AsyncPagedIterator[BasicRelationship]
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
def query_twins(query_expression: QueryExpression,
                max_items_per_page: Optional[int] = None,
                **kwargs: Any) -> AsyncPagedIterator[Dict[str, Any]]
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
async def get_model(model_id: ModelId,
                    include_base_model_contents: bool = False,
                    **kwargs: Any) -> DigitalTwinsModelData
```

Get a model.

**Arguments**:

- `model_id` - The ID of the model.
- `include_base_model_contents` - Whether to include the model (inherited) model contents.
- `**kwargs` - Additional request options.
  

**Returns**:

  The model data.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.list_models"></a>

#### list\_models

```python
def list_models(dependencies_for: Optional[Union[str, List[str]]] = None,
                include_model_definition: bool = False,
                results_per_page: Optional[int] = None,
                **kwargs: Any) -> AsyncPagedIterator[DigitalTwinsModelData]
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
async def create_models(dtdl_models: List[DtdlInterface],
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
async def decommission_model(model_id: ModelId, **kwargs: Any) -> None
```

Decommission a model.

**Arguments**:

- `model_id` - The ID of the model.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.delete_model"></a>

#### delete\_model

```python
async def delete_model(model_id: ModelId, **kwargs: Any) -> None
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
                       model_id: Optional[ModelId] = None,
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
async def publish_telemetry(digital_twin_id: DigitalTwinId,
                            telemetry: TelemetryPayload,
                            message_id: Optional[MessageId] = None,
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
async def publish_component_telemetry(digital_twin_id: DigitalTwinId,
                                      component_name: ComponentName,
                                      telemetry: TelemetryPayload,
                                      message_id: Optional[MessageId] = None,
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
def list_import_jobs(**kwargs: Any) -> AsyncPagedIterator[ImportJob]
```

List import jobs.

**Arguments**:

- `**kwargs` - Additional request options.
  

**Returns**:

  An async iterator over the import jobs.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.get_import_job"></a>

#### get\_import\_job

```python
async def get_import_job(job_id: JobId, **kwargs: Any) -> ImportJob
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
async def create_import_job(job_id: JobId, import_job: Dict[str, Any],
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
async def delete_import_job(job_id: JobId, **kwargs: Any) -> None
```

Delete an import job.

**Arguments**:

- `job_id` - The ID of the job.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.cancel_import_job"></a>

#### cancel\_import\_job

```python
async def cancel_import_job(job_id: JobId, **kwargs: Any) -> ImportJob
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
def list_delete_jobs(**kwargs: Any) -> AsyncPagedIterator[DeleteJob]
```

List delete jobs.

**Arguments**:

- `**kwargs` - Additional request options.
  

**Returns**:

  An async iterator over the delete jobs.

<a id="konnektr_graph.aio.client.KonnektrGraphClient.get_delete_job"></a>

#### get\_delete\_job

```python
async def get_delete_job(job_id: JobId, **kwargs: Any) -> DeleteJob
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
async def create_delete_job(job_id: JobId,
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

<a id="konnektr_graph.aio"></a>

# konnektr\_graph.aio

Async Konnektr Graph SDK.

<a id="konnektr_graph.auth.async_client_secret_credential"></a>

# konnektr\_graph.auth.async\_client\_secret\_credential

AsyncClientSecretCredential for OAuth 2.0 client credentials flow.

<a id="konnektr_graph.auth.async_client_secret_credential.AsyncClientSecretCredential"></a>

## AsyncClientSecretCredential Objects

```python
class AsyncClientSecretCredential()
```

Authenticates using OAuth 2.0 client credentials flow asynchronously.

**Arguments**:

- `domain`: The OAuth provider domain (e.g., 'auth.konnektr.io')
- `audience`: The API audience/resource identifier
- `client_id`: The application client ID
- `client_secret`: The application client secret
- `timeout`: Request timeout in seconds (default: 30)

<a id="konnektr_graph.auth.async_client_secret_credential.AsyncClientSecretCredential.get_token"></a>

#### get\_token

```python
async def get_token() -> str
```

Get the current access token, refreshing if expired or about to expire.

**Raises**:

- `Exception`: If token acquisition fails.

**Returns**:

A valid access token.

<a id="konnektr_graph.auth.async_client_secret_credential.AsyncClientSecretCredential.get_headers"></a>

#### get\_headers

```python
async def get_headers() -> Dict[str, str]
```

Get HTTP headers including the Authorization header.

**Returns**:

Dictionary with Authorization header.

<a id="konnektr_graph.auth.async_device_code_credential"></a>

# konnektr\_graph.auth.async\_device\_code\_credential

AsyncDeviceCodeCredential for OAuth 2.0 device authorization flow.

<a id="konnektr_graph.auth.async_device_code_credential.AsyncDeviceCodeCredential"></a>

## AsyncDeviceCodeCredential Objects

```python
class AsyncDeviceCodeCredential()
```

Authenticates users through the device code flow asynchronously.

**Arguments**:

- `domain`: The OAuth provider domain (e.g., 'auth.konnektr.io')
- `audience`: The API audience/resource identifier
- `client_id`: The application client ID (public client)
- `scope`: OAuth scopes to request (default: 'openid profile email')
- `prompt_callback`: Optional callback for displaying auth instructions.
If not provided, instructions are printed and browser is opened.
- `timeout`: Request timeout in seconds (default: 30)

<a id="konnektr_graph.auth.async_device_code_credential.AsyncDeviceCodeCredential.get_token"></a>

#### get\_token

```python
async def get_token() -> str
```

Get the current access token, initiating device code flow if needed.

**Raises**:

- `Exception`: If authentication fails or times out.

**Returns**:

A valid access token.

<a id="konnektr_graph.auth.async_device_code_credential.AsyncDeviceCodeCredential.get_headers"></a>

#### get\_headers

```python
async def get_headers() -> Dict[str, str]
```

Get HTTP headers including the Authorization header.

**Returns**:

Dictionary with Authorization header.

<a id="konnektr_graph.auth.client_secret_credential"></a>

# konnektr\_graph.auth.client\_secret\_credential

ClientSecretCredential for OAuth 2.0 client credentials flow.

<a id="konnektr_graph.auth.client_secret_credential.ClientSecretCredential"></a>

## ClientSecretCredential Objects

```python
class ClientSecretCredential()
```

Authenticates using OAuth 2.0 client credentials flow.

This credential is intended for service-to-service authentication
where a client_id and client_secret are available.

**Arguments**:

- `domain`: The OAuth provider domain (e.g., 'auth.konnektr.io')
- `audience`: The API audience/resource identifier
- `client_id`: The application client ID
- `client_secret`: The application client secret
- `timeout`: Request timeout in seconds (default: 30)

<a id="konnektr_graph.auth.client_secret_credential.ClientSecretCredential.get_token"></a>

#### get\_token

```python
def get_token() -> str
```

Get the current access token, refreshing if expired or about to expire.

**Raises**:

- `Exception`: If token acquisition fails.

**Returns**:

A valid access token.

<a id="konnektr_graph.auth.client_secret_credential.ClientSecretCredential.get_headers"></a>

#### get\_headers

```python
def get_headers() -> Dict[str, str]
```

Get HTTP headers including the Authorization header.

**Returns**:

Dictionary with Authorization header.

<a id="konnektr_graph.auth.device_code_credential"></a>

# konnektr\_graph.auth.device\_code\_credential

DeviceCodeCredential for OAuth 2.0 device authorization flow.

<a id="konnektr_graph.auth.device_code_credential.DeviceCodeCredential"></a>

## DeviceCodeCredential Objects

```python
class DeviceCodeCredential()
```

Authenticates users through the device code flow.

This credential is intended for interactive authentication in environments
where a browser may not be available (e.g., SSH sessions, CLI tools).

**Arguments**:

- `domain`: The OAuth provider domain (e.g., 'auth.konnektr.io')
- `audience`: The API audience/resource identifier
- `client_id`: The application client ID (public client)
- `scope`: OAuth scopes to request (default: 'openid profile email')
- `prompt_callback`: Optional callback for displaying auth instructions.
If not provided, instructions are printed and browser is opened.
- `timeout`: Request timeout in seconds (default: 30)

<a id="konnektr_graph.auth.device_code_credential.DeviceCodeCredential.get_token"></a>

#### get\_token

```python
def get_token() -> str
```

Get the current access token, initiating device code flow if needed.

**Raises**:

- `Exception`: If authentication fails or times out.

**Returns**:

A valid access token.

<a id="konnektr_graph.auth.device_code_credential.DeviceCodeCredential.get_headers"></a>

#### get\_headers

```python
def get_headers() -> Dict[str, str]
```

Get HTTP headers including the Authorization header.

**Returns**:

Dictionary with Authorization header.

<a id="konnektr_graph.auth.protocol"></a>

# konnektr\_graph.auth.protocol

TokenProvider protocol for Konnektr Graph authentication.

<a id="konnektr_graph.auth.protocol.TokenProvider"></a>

## TokenProvider Objects

```python
@runtime_checkable
class TokenProvider(Protocol)
```

Protocol that all credential classes must implement.

<a id="konnektr_graph.auth.protocol.TokenProvider.get_token"></a>

#### get\_token

```python
def get_token() -> str
```

Get the current access token, refreshing if necessary.

<a id="konnektr_graph.auth.protocol.TokenProvider.get_headers"></a>

#### get\_headers

```python
def get_headers() -> Dict[str, str]
```

Get HTTP headers including the Authorization header.

<a id="konnektr_graph.auth.protocol.AsyncTokenProvider"></a>

## AsyncTokenProvider Objects

```python
@runtime_checkable
class AsyncTokenProvider(Protocol)
```

Protocol for async credential classes.

<a id="konnektr_graph.auth.protocol.AsyncTokenProvider.get_token"></a>

#### get\_token

```python
async def get_token() -> str
```

Get the current access token, refreshing if necessary.

<a id="konnektr_graph.auth.protocol.AsyncTokenProvider.get_headers"></a>

#### get\_headers

```python
async def get_headers() -> Dict[str, str]
```

Get HTTP headers including the Authorization header.

<a id="konnektr_graph.auth.static_token_credential"></a>

# konnektr\_graph.auth.static\_token\_credential

StaticTokenCredential for using a pre-obtained access token.

<a id="konnektr_graph.auth.static_token_credential.StaticTokenCredential"></a>

## StaticTokenCredential Objects

```python
class StaticTokenCredential()
```

Uses a pre-obtained access token directly.

This credential is useful when you already have a valid token from
another source (e.g., a different auth flow, token exchange, etc.).

**Arguments**:

- `token`: The access token to use
- `expires_on`: Optional Unix timestamp when the token expires.
If not provided, the token is assumed to never expire.

<a id="konnektr_graph.auth.static_token_credential.StaticTokenCredential.get_token"></a>

#### get\_token

```python
def get_token() -> str
```

Get the access token.

**Raises**:

- `Exception`: If the token has expired.

**Returns**:

The access token.

<a id="konnektr_graph.auth.static_token_credential.StaticTokenCredential.get_headers"></a>

#### get\_headers

```python
def get_headers() -> Dict[str, str]
```

Get HTTP headers including the Authorization header.

**Returns**:

Dictionary with Authorization header.

<a id="konnektr_graph.auth.static_token_credential.StaticTokenCredential.is_expired"></a>

#### is\_expired

```python
@property
def is_expired() -> bool
```

Check if the token has expired.

<a id="konnektr_graph.auth"></a>

# konnektr\_graph.auth

Authentication modules for Konnektr Graph SDK.

<a id="konnektr_graph.client"></a>

# konnektr\_graph.client

Konnektr Graph SDK (Azure-free) - Synchronous Client

<a id="konnektr_graph.client.PagedIterator"></a>

## PagedIterator Objects

```python
class PagedIterator(Iterator[T], Generic[T])
```

Iterator for handling paged responses.
Supports both nextLink in body and x-ms-continuation in headers.

<a id="konnektr_graph.client.PagedIterator.__init__"></a>

#### \_\_init\_\_

```python
def __init__(client: "KonnektrGraphClient",
             initial_url: str,
             method: str = "GET",
             headers: Optional[Dict[str, str]] = None,
             json_data: Optional[Dict[str, Any]] = None,
             params: Optional[Dict[str, Any]] = None,
             model_cls: Optional[Type[T]] = None,
             items_key: str = "value")
```

Initialize the paged iterator.

**Arguments**:

- `client` - The KonnektrGraphClient instance.
- `initial_url` - The initial URL for the first page.
- `method` - The HTTP method to use. Defaults to "GET".
- `headers` - Optional headers to include in the request.
- `json_data` - Optional JSON body for the request.
- `params` - Optional query parameters for the request.
- `model_cls` - Optional class to instantiate for each item in the results.
- `items_key` - The key in the JSON response that contains the items list. Defaults to "value".

<a id="konnektr_graph.client.KonnektrGraphClient"></a>

## KonnektrGraphClient Objects

```python
class KonnektrGraphClient()
```

<a id="konnektr_graph.client.KonnektrGraphClient.__init__"></a>

#### \_\_init\_\_

```python
def __init__(endpoint: str, credential: TokenProvider)
```

Initialize the Konnektr Graph Client.

**Arguments**:

- `endpoint` - API endpoint (e.g. https://graph.konnektr.io)
- `credential` - TokenProvider credential for authentication.

<a id="konnektr_graph.client.KonnektrGraphClient.get_digital_twin"></a>

#### get\_digital\_twin

```python
def get_digital_twin(digital_twin_id: DigitalTwinId,
                     **kwargs: Any) -> BasicDigitalTwin
```

Get a digital twin by ID.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `**kwargs` - Additional request parameters.
  

**Returns**:

  The digital twin as BasicDigitalTwin.

<a id="konnektr_graph.client.KonnektrGraphClient.upsert_digital_twin"></a>

#### upsert\_digital\_twin

```python
def upsert_digital_twin(digital_twin_id: DigitalTwinId,
                        digital_twin: BasicDigitalTwin,
                        **kwargs: Any) -> BasicDigitalTwin
```

Create or update a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `digital_twin` - The digital twin data to create or update.
- `**kwargs` - Additional request options.
  

**Returns**:

  The created or updated digital twin data.

<a id="konnektr_graph.client.KonnektrGraphClient.update_digital_twin"></a>

#### update\_digital\_twin

```python
def update_digital_twin(digital_twin_id: DigitalTwinId,
                        json_patch: List[JsonPatchOperation],
                        **kwargs: Any) -> None
```

Update a digital twin (JSON Patch).

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `json_patch` - The JSON patch to apply.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.client.KonnektrGraphClient.delete_digital_twin"></a>

#### delete\_digital\_twin

```python
def delete_digital_twin(digital_twin_id: DigitalTwinId, **kwargs: Any) -> None
```

Delete a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.client.KonnektrGraphClient.get_component"></a>

#### get\_component

```python
def get_component(digital_twin_id: DigitalTwinId,
                  component_name: ComponentName,
                  **kwargs: Any) -> BasicDigitalTwinComponent
```

Get a component from a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `component_name` - The name of the component.
- `**kwargs` - Additional request parameters.
  

**Returns**:

  The component data.

<a id="konnektr_graph.client.KonnektrGraphClient.update_component"></a>

#### update\_component

```python
def update_component(digital_twin_id: DigitalTwinId,
                     component_name: ComponentName,
                     json_patch: List[JsonPatchOperation],
                     **kwargs: Any) -> None
```

Update a component.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `component_name` - The name of the component.
- `json_patch` - The JSON patch to apply.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.client.KonnektrGraphClient.get_relationship"></a>

#### get\_relationship

```python
def get_relationship(digital_twin_id: DigitalTwinId,
                     relationship_id: RelationshipId,
                     **kwargs: Any) -> BasicRelationship
```

Get a relationship by ID.

**Arguments**:

- `digital_twin_id` - The ID of the source digital twin.
- `relationship_id` - The ID of the relationship.
- `**kwargs` - Additional request parameters.
  

**Returns**:

  The relationship data.

<a id="konnektr_graph.client.KonnektrGraphClient.upsert_relationship"></a>

#### upsert\_relationship

```python
def upsert_relationship(digital_twin_id: DigitalTwinId,
                        relationship_id: RelationshipId,
                        relationship: BasicRelationship,
                        **kwargs: Any) -> BasicRelationship
```

Create or update a relationship.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `relationship_id` - The ID of the relationship.
- `relationship` - The relationship data.
- `**kwargs` - Additional request options.
  

**Returns**:

  The created or updated relationship data.

<a id="konnektr_graph.client.KonnektrGraphClient.update_relationship"></a>

#### update\_relationship

```python
def update_relationship(digital_twin_id: DigitalTwinId,
                        relationship_id: RelationshipId,
                        json_patch: List[JsonPatchOperation],
                        **kwargs: Any) -> None
```

Update a relationship.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `relationship_id` - The ID of the relationship.
- `json_patch` - The JSON patch to apply.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.client.KonnektrGraphClient.delete_relationship"></a>

#### delete\_relationship

```python
def delete_relationship(digital_twin_id: DigitalTwinId,
                        relationship_id: RelationshipId,
                        **kwargs: Any) -> None
```

Delete a relationship.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `relationship_id` - The ID of the relationship.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.client.KonnektrGraphClient.list_relationships"></a>

#### list\_relationships

```python
def list_relationships(digital_twin_id: DigitalTwinId,
                       relationship_name: Optional[RelationshipName] = None,
                       **kwargs: Any) -> PagedIterator[BasicRelationship]
```

List relationships for a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `relationship_name` - Optional name of the relationship to filter by.
- `**kwargs` - Additional request options.
  

**Returns**:

  An iterator over the relationships.

<a id="konnektr_graph.client.KonnektrGraphClient.list_incoming_relationships"></a>

#### list\_incoming\_relationships

```python
def list_incoming_relationships(
        digital_twin_id: DigitalTwinId,
        **kwargs: Any) -> PagedIterator[BasicRelationship]
```

List incoming relationships for a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `**kwargs` - Additional request options.
  

**Returns**:

  An iterator over the incoming relationships.

<a id="konnektr_graph.client.KonnektrGraphClient.query_twins"></a>

#### query\_twins

```python
def query_twins(query_expression: QueryExpression,
                max_items_per_page: Optional[int] = None,
                **kwargs: Any) -> PagedIterator[Dict[str, Any]]
```

Query digital twins.

**Arguments**:

- `query_expression` - The query expression.
- `max_items_per_page` - Optional maximum items per page.
- `**kwargs` - Additional request options.
  

**Returns**:

  An iterator over the query results.

<a id="konnektr_graph.client.KonnektrGraphClient.get_model"></a>

#### get\_model

```python
def get_model(model_id: ModelId,
              include_base_model_contents: bool = False,
              **kwargs: Any) -> DigitalTwinsModelData
```

Get a model.

**Arguments**:

- `model_id` - The ID of the model.
- `include_base_model_contents` - Whether to include the model (inherited) model contents.
- `**kwargs` - Additional request options.
  

**Returns**:

  The model data.

<a id="konnektr_graph.client.KonnektrGraphClient.list_models"></a>

#### list\_models

```python
def list_models(dependencies_for: Optional[Union[ModelId,
                                                 List[ModelId]]] = None,
                include_model_definition: bool = False,
                results_per_page: Optional[int] = None,
                **kwargs: Any) -> PagedIterator[DigitalTwinsModelData]
```

List models.

**Arguments**:

- `dependencies_for` - Optional model ID or list of model IDs to get dependencies for.
- `include_model_definition` - Whether to include the model definition.
- `results_per_page` - Optional maximum items per page.
- `**kwargs` - Additional request options.
  

**Returns**:

  An iterator over the models.

<a id="konnektr_graph.client.KonnektrGraphClient.create_models"></a>

#### create\_models

```python
def create_models(dtdl_models: List[DtdlInterface],
                  **kwargs: Any) -> List[DigitalTwinsModelData]
```

Create models.

**Arguments**:

- `dtdl_models` - A list of DTDL model definitions.
- `**kwargs` - Additional request options.
  

**Returns**:

  A list of created model data.

<a id="konnektr_graph.client.KonnektrGraphClient.decommission_model"></a>

#### decommission\_model

```python
def decommission_model(model_id: ModelId, **kwargs: Any) -> None
```

Decommission a model.

**Arguments**:

- `model_id` - The ID of the model.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.client.KonnektrGraphClient.delete_model"></a>

#### delete\_model

```python
def delete_model(model_id: ModelId, **kwargs: Any) -> None
```

Delete a model.

**Arguments**:

- `model_id` - The ID of the model.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.client.KonnektrGraphClient.search_models"></a>

#### search\_models

```python
def search_models(search_text: str,
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

<a id="konnektr_graph.client.KonnektrGraphClient.search_twins"></a>

#### search\_twins

```python
def search_twins(search_text: str,
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

<a id="konnektr_graph.client.KonnektrGraphClient.publish_telemetry"></a>

#### publish\_telemetry

```python
def publish_telemetry(digital_twin_id: DigitalTwinId,
                      telemetry: TelemetryPayload,
                      message_id: Optional[MessageId] = None,
                      **kwargs: Any) -> None
```

Publish telemetry for a digital twin.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `telemetry` - The telemetry data.
- `message_id` - Optional unique identifier for the telemetry message.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.client.KonnektrGraphClient.publish_component_telemetry"></a>

#### publish\_component\_telemetry

```python
def publish_component_telemetry(digital_twin_id: DigitalTwinId,
                                component_name: ComponentName,
                                telemetry: TelemetryPayload,
                                message_id: Optional[MessageId] = None,
                                **kwargs: Any) -> None
```

Publish telemetry for a component.

**Arguments**:

- `digital_twin_id` - The ID of the digital twin.
- `component_name` - The name of the component.
- `telemetry` - The telemetry data.
- `message_id` - Optional unique identifier for the telemetry message.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.client.KonnektrGraphClient.list_import_jobs"></a>

#### list\_import\_jobs

```python
def list_import_jobs(**kwargs: Any) -> PagedIterator[ImportJob]
```

List import jobs.

**Arguments**:

- `**kwargs` - Additional request options.
  

**Returns**:

  An iterator over the import jobs.

<a id="konnektr_graph.client.KonnektrGraphClient.get_import_job"></a>

#### get\_import\_job

```python
def get_import_job(job_id: JobId, **kwargs: Any) -> ImportJob
```

Get an import job.

**Arguments**:

- `job_id` - The ID of the job.
- `**kwargs` - Additional request options.
  

**Returns**:

  The import job data.

<a id="konnektr_graph.client.KonnektrGraphClient.create_import_job"></a>

#### create\_import\_job

```python
def create_import_job(job_id: JobId, import_job: Dict[str, Any],
                      **kwargs: Any) -> ImportJob
```

Create an import job.

**Arguments**:

- `job_id` - The ID of the job.
- `import_job` - The import job data.
- `**kwargs` - Additional request options.
  

**Returns**:

  The created import job data.

<a id="konnektr_graph.client.KonnektrGraphClient.delete_import_job"></a>

#### delete\_import\_job

```python
def delete_import_job(job_id: JobId, **kwargs: Any) -> None
```

Delete an import job.

**Arguments**:

- `job_id` - The ID of the job.
- `**kwargs` - Additional request options.

<a id="konnektr_graph.client.KonnektrGraphClient.cancel_import_job"></a>

#### cancel\_import\_job

```python
def cancel_import_job(job_id: JobId, **kwargs: Any) -> ImportJob
```

Cancel an import job.

**Arguments**:

- `job_id` - The ID of the job.
- `**kwargs` - Additional request options.
  

**Returns**:

  The cancelled import job data.

<a id="konnektr_graph.client.KonnektrGraphClient.list_delete_jobs"></a>

#### list\_delete\_jobs

```python
def list_delete_jobs(**kwargs: Any) -> PagedIterator[DeleteJob]
```

List delete jobs.

**Arguments**:

- `**kwargs` - Additional request options.
  

**Returns**:

  An iterator over the delete jobs.

<a id="konnektr_graph.client.KonnektrGraphClient.get_delete_job"></a>

#### get\_delete\_job

```python
def get_delete_job(job_id: JobId, **kwargs: Any) -> DeleteJob
```

Get a delete job.

**Arguments**:

- `job_id` - The ID of the job.
- `**kwargs` - Additional request options.
  

**Returns**:

  The delete job data.

<a id="konnektr_graph.client.KonnektrGraphClient.create_delete_job"></a>

#### create\_delete\_job

```python
def create_delete_job(job_id: JobId,
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

<a id="konnektr_graph.exceptions"></a>

# konnektr\_graph.exceptions

Custom exceptions for Konnektr Graph SDK.

<a id="konnektr_graph.exceptions.KonnektrGraphError"></a>

## KonnektrGraphError Objects

```python
class KonnektrGraphError(Exception)
```

Base exception for all Konnektr Graph errors.

<a id="konnektr_graph.exceptions.HttpResponseError"></a>

## HttpResponseError Objects

```python
class HttpResponseError(KonnektrGraphError)
```

Raised when an HTTP response is not successful.

<a id="konnektr_graph.exceptions.ResourceNotFoundError"></a>

## ResourceNotFoundError Objects

```python
class ResourceNotFoundError(HttpResponseError)
```

Raised when a resource is not found (404).

<a id="konnektr_graph.exceptions.ResourceExistsError"></a>

## ResourceExistsError Objects

```python
class ResourceExistsError(HttpResponseError)
```

Raised when a resource already exists (409).

<a id="konnektr_graph.exceptions.AuthenticationError"></a>

## AuthenticationError Objects

```python
class AuthenticationError(HttpResponseError)
```

Raised when authentication fails (401/403).

<a id="konnektr_graph.exceptions.ValidationError"></a>

## ValidationError Objects

```python
class ValidationError(KonnektrGraphError)
```

Raised when input validation fails.

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
- `created_date_time` - The date and time the job was created (ISO 8601 format).
- `last_action_date_time` - The date and time of the last action (ISO 8601 format).
- `finished_date_time` - The date and time the job finished (ISO 8601 format).
- `purge_date_time` - The date and time the job will be purged (ISO 8601 format).
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

<a id="konnektr_graph.models.ImportJob.to_dict"></a>

#### to\_dict

```python
def to_dict() -> Dict[str, Any]
```

Convert the ImportJob instance to a dictionary.

**Returns**:

  A dictionary representation of the ImportJob.

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
- `created_date_time` - The date and time the job was created (ISO 8601 format).
- `last_action_date_time` - The date and time of the last action (ISO 8601 format).
- `finished_date_time` - The date and time the job finished (ISO 8601 format).
- `purge_date_time` - The date and time the job will be purged (ISO 8601 format).
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

<a id="konnektr_graph.models.DeleteJob.to_dict"></a>

#### to\_dict

```python
def to_dict() -> Dict[str, Any]
```

Convert the DeleteJob instance to a dictionary.

**Returns**:

  A dictionary representation of the DeleteJob.

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
- `upload_time` - The date and time the model was uploaded (ISO 8601 format).
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

<a id="konnektr_graph.models.DigitalTwinsModelData.to_dict"></a>

#### to\_dict

```python
def to_dict() -> Dict[str, Any]
```

Convert the DigitalTwinsModelData instance to a dictionary.

**Returns**:

  A dictionary representation of the DigitalTwinsModelData.

<a id="konnektr_graph.types"></a>

# konnektr\_graph.types

Type definitions and aliases for the Konnektr Graph SDK.

<a id="konnektr_graph.types.DigitalTwinMetadata"></a>

## DigitalTwinMetadata Objects

```python
@dataclass
class DigitalTwinMetadata()
```

Metadata for a digital twin.

**Attributes**:

- `model` - The model ID (e.g., dtmi:com:example:Room;1).
- `metadata` - Additional metadata properties.

<a id="konnektr_graph.types.DigitalTwinMetadata.model"></a>

#### model

Represents $model in JSON

<a id="konnektr_graph.types.DigitalTwinMetadata.metadata"></a>

#### metadata

Additional metadata

<a id="konnektr_graph.types.BasicDigitalTwin"></a>

## BasicDigitalTwin Objects

```python
@dataclass
class BasicDigitalTwin()
```

A structured digital twin following the Azure Digital Twins BasicDigitalTwin pattern.

This class provides proper typing and validation for digital twin data,
making it compatible with MCP schema generation for LLMs.

**Attributes**:

- `dtId` - The unique ID of the digital twin.
- `metadata` - Information about the model this twin conforms to.
- `etag` - Optional ETag for concurrency control.
- `lastUpdateTime` - Optional timestamp of last update.
- `contents` - Additional properties defined in the DTDL model.

<a id="konnektr_graph.types.BasicDigitalTwin.dtId"></a>

#### dtId

Represents $dtId in JSON

<a id="konnektr_graph.types.BasicDigitalTwin.metadata"></a>

#### metadata

Represents $metadata in JSON

<a id="konnektr_graph.types.BasicDigitalTwin.etag"></a>

#### etag

Represents $etag in JSON

<a id="konnektr_graph.types.BasicDigitalTwin.lastUpdateTime"></a>

#### lastUpdateTime

Represents $lastUpdateTime in JSON

<a id="konnektr_graph.types.BasicDigitalTwin.contents"></a>

#### contents

Custom properties and components

<a id="konnektr_graph.types.BasicDigitalTwin.from_dict"></a>

#### from\_dict

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> "BasicDigitalTwin"
```

Create a BasicDigitalTwin from a dictionary with $ prefixed keys.

<a id="konnektr_graph.types.BasicDigitalTwin.to_dict"></a>

#### to\_dict

```python
def to_dict() -> Dict[str, Any]
```

Convert to a dictionary with $ prefixed keys.

<a id="konnektr_graph.types.BasicRelationship"></a>

## BasicRelationship Objects

```python
@dataclass
class BasicRelationship()
```

A structured relationship following the Azure Digital Twins BasicRelationship pattern.

This class provides proper typing and validation for relationship data,
making it compatible with MCP schema generation for LLMs.

**Attributes**:

- `relationshipId` - The unique ID of the relationship.
- `sourceId` - The ID of the source digital twin.
- `targetId` - The ID of the target digital twin.
- `relationshipName` - The name/type of the relationship (e.g., "contains", "isPartOf").
- `etag` - Optional ETag for concurrency control.
- `properties` - Additional custom properties defined in the DTDL model.

<a id="konnektr_graph.types.BasicRelationship.relationshipId"></a>

#### relationshipId

Represents $relationshipId in JSON

<a id="konnektr_graph.types.BasicRelationship.sourceId"></a>

#### sourceId

Represents $sourceId in JSON

<a id="konnektr_graph.types.BasicRelationship.targetId"></a>

#### targetId

Represents $targetId in JSON

<a id="konnektr_graph.types.BasicRelationship.relationshipName"></a>

#### relationshipName

Represents $relationshipName in JSON

<a id="konnektr_graph.types.BasicRelationship.etag"></a>

#### etag

Represents $etag in JSON

<a id="konnektr_graph.types.BasicRelationship.properties"></a>

#### properties

Custom relationship properties

<a id="konnektr_graph.types.BasicRelationship.from_dict"></a>

#### from\_dict

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> "BasicRelationship"
```

Create a BasicRelationship from a dictionary with $ prefixed keys.

<a id="konnektr_graph.types.BasicRelationship.to_dict"></a>

#### to\_dict

```python
def to_dict() -> Dict[str, Any]
```

Convert to a dictionary with $ prefixed keys.

<a id="konnektr_graph.types.BasicDigitalTwinComponent"></a>

## BasicDigitalTwinComponent Objects

```python
@dataclass
class BasicDigitalTwinComponent()
```

A component within a digital twin.

Components are nested objects within a digital twin that have their own metadata.

**Attributes**:

- `metadata` - Metadata about the component.
- `properties` - Component properties defined in the DTDL model.

<a id="konnektr_graph.types.BasicDigitalTwinComponent.metadata"></a>

#### metadata

Represents $metadata in JSON

<a id="konnektr_graph.types.BasicDigitalTwinComponent.properties"></a>

#### properties

Custom component properties

<a id="konnektr_graph.types.BasicDigitalTwinComponent.from_dict"></a>

#### from\_dict

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> "BasicDigitalTwinComponent"
```

Create a BasicDigitalTwinComponent from a dictionary.

<a id="konnektr_graph.types.BasicDigitalTwinComponent.to_dict"></a>

#### to\_dict

```python
def to_dict() -> Dict[str, Any]
```

Convert to a dictionary with $ prefixed keys.

<a id="konnektr_graph.types.DtdlLocalizableString"></a>

#### DtdlLocalizableString

string or {countryCode: string}

<a id="konnektr_graph.types.DtdlEnumValue"></a>

## DtdlEnumValue Objects

```python
@dataclass
class DtdlEnumValue()
```

A value in a DTDL enum schema.

<a id="konnektr_graph.types.DtdlEnumValue.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlEnumSchema"></a>

## DtdlEnumSchema Objects

```python
@dataclass
class DtdlEnumSchema()
```

A DTDL enum schema definition.

<a id="konnektr_graph.types.DtdlEnumSchema.type"></a>

#### type

Represents @type in JSON

<a id="konnektr_graph.types.DtdlEnumSchema.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlMapKey"></a>

## DtdlMapKey Objects

```python
@dataclass
class DtdlMapKey()
```

Key definition for a DTDL map schema.

<a id="konnektr_graph.types.DtdlMapKey.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlMapValue"></a>

## DtdlMapValue Objects

```python
@dataclass
class DtdlMapValue()
```

Value definition for a DTDL map schema.

<a id="konnektr_graph.types.DtdlMapValue.schema"></a>

#### schema

Can be primitive string or complex schema

<a id="konnektr_graph.types.DtdlMapValue.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlMapSchema"></a>

## DtdlMapSchema Objects

```python
@dataclass
class DtdlMapSchema()
```

A DTDL map schema definition.

<a id="konnektr_graph.types.DtdlMapSchema.type"></a>

#### type

Represents @type in JSON

<a id="konnektr_graph.types.DtdlMapSchema.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlObjectField"></a>

## DtdlObjectField Objects

```python
@dataclass
class DtdlObjectField()
```

A field in a DTDL object schema.

<a id="konnektr_graph.types.DtdlObjectField.schema"></a>

#### schema

Can be primitive string or complex schema

<a id="konnektr_graph.types.DtdlObjectField.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlObjectField.type"></a>

#### type

Represents @type in JSON

<a id="konnektr_graph.types.DtdlObjectSchema"></a>

## DtdlObjectSchema Objects

```python
@dataclass
class DtdlObjectSchema()
```

A DTDL object schema definition.

<a id="konnektr_graph.types.DtdlObjectSchema.type"></a>

#### type

Represents @type in JSON

<a id="konnektr_graph.types.DtdlObjectSchema.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlArraySchema"></a>

## DtdlArraySchema Objects

```python
@dataclass
class DtdlArraySchema()
```

A DTDL array schema definition.

<a id="konnektr_graph.types.DtdlArraySchema.type"></a>

#### type

Represents @type in JSON

<a id="konnektr_graph.types.DtdlArraySchema.elementSchema"></a>

#### elementSchema

Can be primitive string or complex schema

<a id="konnektr_graph.types.DtdlArraySchema.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlProperty"></a>

## DtdlProperty Objects

```python
@dataclass
class DtdlProperty()
```

A DTDL property definition.

<a id="konnektr_graph.types.DtdlProperty.schema"></a>

#### schema

Can be primitive string or complex schema

<a id="konnektr_graph.types.DtdlProperty.type"></a>

#### type

Represents @type in JSON

<a id="konnektr_graph.types.DtdlProperty.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlProperty.overrides"></a>

#### overrides

Overriding extension

<a id="konnektr_graph.types.DtdlProperty.annotates"></a>

#### annotates

Annotation extension

<a id="konnektr_graph.types.DtdlRelationship"></a>

## DtdlRelationship Objects

```python
@dataclass
class DtdlRelationship()
```

A DTDL relationship definition.

<a id="konnektr_graph.types.DtdlRelationship.type"></a>

#### type

Represents @type in JSON

<a id="konnektr_graph.types.DtdlRelationship.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlTelemetry"></a>

## DtdlTelemetry Objects

```python
@dataclass
class DtdlTelemetry()
```

A DTDL telemetry definition.

<a id="konnektr_graph.types.DtdlTelemetry.schema"></a>

#### schema

Can be primitive string or complex schema

<a id="konnektr_graph.types.DtdlTelemetry.type"></a>

#### type

Represents @type in JSON

<a id="konnektr_graph.types.DtdlTelemetry.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlComponent"></a>

## DtdlComponent Objects

```python
@dataclass
class DtdlComponent()
```

A DTDL component definition.

<a id="konnektr_graph.types.DtdlComponent.schema"></a>

#### schema

Reference to another Interface

<a id="konnektr_graph.types.DtdlComponent.type"></a>

#### type

Represents @type in JSON

<a id="konnektr_graph.types.DtdlComponent.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlCommand"></a>

## DtdlCommand Objects

```python
@dataclass
class DtdlCommand()
```

A DTDL command definition.

<a id="konnektr_graph.types.DtdlCommand.type"></a>

#### type

Represents @type in JSON

<a id="konnektr_graph.types.DtdlCommand.request"></a>

#### request

Request schema

<a id="konnektr_graph.types.DtdlCommand.response"></a>

#### response

Response schema

<a id="konnektr_graph.types.DtdlCommand.id"></a>

#### id

Represents @id in JSON

<a id="konnektr_graph.types.DtdlInterface"></a>

## DtdlInterface Objects

```python
@dataclass
class DtdlInterface()
```

A DTDL Interface definition (v3 & v4).

This represents a complete Digital Twins model definition.

<a id="konnektr_graph.types.DtdlInterface.id"></a>

#### id

Represents @id in JSON (e.g., "dtmi:com:example:Room;1")

<a id="konnektr_graph.types.DtdlInterface.type"></a>

#### type

Represents @type in JSON

<a id="konnektr_graph.types.DtdlInterface.context"></a>

#### context

Represents @context in JSON

<a id="konnektr_graph.types.ErrorDict"></a>

## ErrorDict Objects

```python
class ErrorDict(TypedDict)
```

TypedDict representing an error response.

