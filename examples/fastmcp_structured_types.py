# Example: Using Structured Types with FastMCP

"""
This example demonstrates how the BasicDigitalTwin and BasicRelationship dataclasses
work with FastMCP for schema generation.

The dataclasses provide structured types that FastMCP can introspect to generate
JSON schemas for LLMs, while still being lightweight and not requiring Pydantic.
"""

from konnektr_graph import (
    KonnektrGraphClient,
    BasicDigitalTwin,
    BasicRelationship,
    DigitalTwinMetadata,
)
from konnektr_graph.auth import StaticTokenCredential

# Initialize client
credential = StaticTokenCredential("your-token-here")
client = KonnektrGraphClient("https://api.example.com", credential)


# Example 1: Creating a BasicDigitalTwin with structured types
def create_room_twin() -> BasicDigitalTwin:
    """
    Create a structured digital twin for a room.
    FastMCP can generate a schema from this return type.
    """
    metadata = DigitalTwinMetadata(model="dtmi:com:example:Room;1")

    twin = BasicDigitalTwin(
        dtId="Room-101",
        metadata=metadata,
        contents={"temperature": 22.5, "humidity": 45.0, "floor": 1},
    )

    # API now accepts BasicDigitalTwin directly
    created = client.upsert_digital_twin("Room-101", twin)

    # Returns BasicDigitalTwin
    return created


# Example 2: Creating a BasicRelationship with structured types
def create_contains_relationship() -> BasicRelationship:
    """
    Create a structured relationship between twins.
    FastMCP can generate a schema from this return type.
    """
    relationship = BasicRelationship(
        relationshipId="rel-001",
        sourceId="Building-1",
        targetId="Room-101",
        relationshipName="contains",
        properties={"createdDate": "2026-01-02T10:00:00Z", "isActive": True},
    )

    # API now accepts BasicRelationship directly
    created = client.upsert_relationship("Building-1", "rel-001", relationship)

    # Returns BasicRelationship
    return created


# Example 3: Using with FastMCP (pseudocode)
"""
from fastmcp import FastMCP

mcp = FastMCP("Digital Twins Server")

@mcp.tool
def get_room(room_id: str) -> BasicDigitalTwin:
    '''
    Get a room digital twin by ID.
    
    FastMCP will automatically generate a JSON schema from the BasicDigitalTwin
    dataclass, including all its fields with proper types.
    '''
    twin_dict = client.get_digital_twin(room_id)
    return BasicDigitalTwin.from_dict(twin_dict)

@mcp.tool
def get_relationship(source_id: str, rel_id: str) -> BasicRelationship:
    '''
    Get a relationship by ID.
    
    FastMCP generates a schema showing the structure of relationships,
    helping the LLM understand the expected format.
    '''
    rel_dict = client.get_relationship(source_id, rel_id)
    return BasicRelationship.from_dict(rel_dict)

@mcp.tool
def create_room(
    room_id: str,
    model_id: str,
    temperature: float,
    humidity: float
) -> BasicDigitalTwin:
    '''
    Create a new room digital twin.
    
    The return type annotation tells FastMCP what structure to expect,
    enabling proper validation and schema generation for the LLM.
    '''
    metadata = DigitalTwinMetadata(model=model_id)
    twin = BasicDigitalTwin(
        dtId=room_id,
        metadata=metadata,
        contents={
            "temperature": temperature,
            "humidity": humidity
        }
    )
    
    twin_dict = twin.to_dict()
    created = client.upsert_digital_twin(room_id, twin_dict)
    return BasicDigitalTwin.from_dict(created)
"""

# Example 4: Working with the data
if __name__ == "__main__":
    # Create a twin using structured types
    twin = BasicDigitalTwin(
        dtId="Sensor-123",
        metadata=DigitalTwinMetadata(model="dtmi:com:example:Sensor;1"),
        contents={"temperature": 23.0},
    )

    # Convert to dict (with $ prefixed keys) for API
    twin_dict = twin.to_dict()
    print("Twin as dict:", twin_dict)
    # Output: {'$dtId': 'Sensor-123', '$metadata': {'$model': 'dtmi:com:example:Sensor;1'}, 'temperature': 23.0}

    # Convert back from dict
    twin_from_dict = BasicDigitalTwin.from_dict(twin_dict)
    print(f"Twin ID: {twin_from_dict.dtId}")
    print(f"Model: {twin_from_dict.metadata.model}")
    print(f"Temperature: {twin_from_dict.contents.get('temperature')}")

    print("\n✅ Dataclasses provide structure for FastMCP schema generation")
    print("✅ No Pydantic dependency required")
    print("✅ Bidirectional conversion between dataclass and dict formats")
