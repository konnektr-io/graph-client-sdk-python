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

