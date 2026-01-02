# Example: Improved Typing in Konnektr Graph SDK

"""
This example demonstrates the significantly improved typing in the library.
All methods now use structured models (BasicDigitalTwin, BasicRelationship) with proper type hints.
"""

from konnektr_graph import (
    KonnektrGraphClient,
    BasicDigitalTwin,
    BasicRelationship,
    DigitalTwinMetadata,
    JsonPatchOperation,
    DigitalTwinId,
    ModelId,
)
from konnektr_graph.auth import StaticTokenCredential

# Initialize client
credential = StaticTokenCredential("your-token-here")
client = KonnektrGraphClient("https://api.example.com", credential)

# Example 1: Type-safe digital twin operations
twin_id: DigitalTwinId = "Building-1"

# Get digital twin - returns BasicDigitalTwin
twin: BasicDigitalTwin = client.get_digital_twin(twin_id)
print(f"Twin ID: {twin.dtId}")
print(f"Twin Model: {twin.metadata.model}")
print(f"Twin ETag: {twin.etag}")

# Example 2: Create structured digital twin
new_twin = BasicDigitalTwin(
    dtId="Sensor-123",
    metadata=DigitalTwinMetadata(model="dtmi:com:example:Sensor;1"),
    contents={"temperature": 22.5, "humidity": 45.0},
)
created_twin: BasicDigitalTwin = client.upsert_digital_twin("Sensor-123", new_twin)

# Example 3: Type-safe JSON patch operations
patch_operations: list[JsonPatchOperation] = [
    {"op": "replace", "path": "/temperature", "value": 23.0},
]
client.update_digital_twin(twin_id, patch_operations)

# Example 4: Type-safe relationship operations
relationship = BasicRelationship(
    relationshipId="rel-001",
    relationshipName="contains",
    sourceId="Building-1",
    targetId="Sensor-123",
    properties={"installedDate": "2024-01-15"},
)
created_rel: BasicRelationship = client.upsert_relationship(
    "Building-1", "rel-001", relationship
)
print(
    f"Created relationship: {created_rel.relationshipName} from {created_rel.sourceId} to {created_rel.targetId}"
)

# Example 5: Type-safe iterators with proper generic types
from konnektr_graph import PagedIterator
from konnektr_graph.models import DigitalTwinsModelData, ImportJob

# List models - properly typed iterator
models_iterator: PagedIterator[DigitalTwinsModelData] = client.list_models(
    include_model_definition=True
)
for model in models_iterator:
    print(f"Model: {model.id} - {model.display_name}")
    # IDE knows 'model' is DigitalTwinsModelData and provides autocomplete

# List import jobs - properly typed iterator
import_jobs: PagedIterator[ImportJob] = client.list_import_jobs()
for job in import_jobs:
    print(f"Job {job.id}: {job.status}")
    # IDE knows 'job' is ImportJob with all its properties

# Example 6: Type-safe query with generic results
query_results: PagedIterator[dict] = client.query_twins(
    "SELECT * FROM DIGITALTWINS WHERE $dtId = 'Building-1'"
)
for result in query_results:
    print(f"Query result: {result}")

# Example 7: Async client with same typing improvements
from konnektr_graph.aio import KonnektrGraphClient as AsyncClient
from konnektr_graph.aio import AsyncPagedIterator


async def async_example():
    async with AsyncClient("https://api.example.com", credential) as async_client:
        # All async methods have the same type safety
        twin: BasicDigitalTwin = await async_client.get_digital_twin("Building-1")
        print(f"Async twin: {twin.dtId} with model {twin.metadata.model}")

        # Async iterators are properly typed
        models: AsyncPagedIterator[DigitalTwinsModelData] = async_client.list_models()
        async for model in models:
            print(f"Model: {model.id}")


print("✅ All operations are now fully type-safe!")
print("✅ IDEs provide accurate autocomplete and type checking")
print(
    "✅ Structured models (BasicDigitalTwin, BasicRelationship) provide clear schema for LLMs"
)
print("✅ Catching type errors at development time instead of runtime")
