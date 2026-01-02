# Example: Working with DTDL Models using structured types

"""
This example demonstrates how to create, parse, and work with
DTDL (Digital Twins Definition Language) models using the structured types.

Supports DTDL v3 and v4: https://github.com/Azure/opendigitaltwins-dtdl
"""

from konnektr_graph import (
    KonnektrGraphClient,
    DtdlInterface,
    DtdlProperty,
    DtdlRelationship,
    DtdlTelemetry,
    DtdlComponent,
    DtdlObjectSchema,
    DtdlObjectField,
    DtdlEnumSchema,
    DtdlEnumValue,
)
from konnektr_graph.auth import StaticTokenCredential

# Initialize client
credential = StaticTokenCredential("your-token-here")
client = KonnektrGraphClient("https://api.example.com", credential)


# Example 1: Creating a complete DTDL Interface
def create_room_model() -> DtdlInterface:
    """Create a Room model with properties, telemetry, and relationships."""

    room_model = DtdlInterface(
        id="dtmi:com:example:Room;1",
        type="Interface",
        context=["dtmi:dtdl:context;3"],
        displayName="Room",
        description="A room in a building with environmental sensors",
        contents=[
            # Property: Floor number
            DtdlProperty(
                name="floor",
                schema="integer",
                type="Property",
                displayName="Floor Number",
                description="The floor on which this room is located",
                writable=False,
            ).to_dict(),
            # Property: Room name with localization
            DtdlProperty(
                name="roomName",
                schema="string",
                type="Property",
                displayName={"en": "Room Name", "nl": "Kamernaam"},
                writable=True,
            ).to_dict(),
            # Telemetry: Temperature
            DtdlTelemetry(
                name="temperature",
                schema="double",
                type="Telemetry",
                displayName="Temperature",
                description="Current temperature in Celsius",
                unit="degreeCelsius",
            ).to_dict(),
            # Telemetry: Humidity
            DtdlTelemetry(
                name="humidity",
                schema="double",
                type="Telemetry",
                displayName="Humidity",
                description="Current relative humidity percentage",
                unit="percent",
            ).to_dict(),
            # Relationship: Contains equipment
            DtdlRelationship(
                name="contains",
                type="Relationship",
                target="dtmi:com:example:Equipment;1",
                displayName="Contains",
                properties=[],
            ).to_dict(),
        ],
    )

    return room_model


# Example 2: Creating a model with complex schemas
def create_sensor_model_with_complex_schemas() -> DtdlInterface:
    """Create a Sensor model with enum and object schemas."""

    # Create an enum schema for sensor status
    status_enum = DtdlEnumSchema(
        type="Enum",
        valueSchema="string",
        enumValues=[
            DtdlEnumValue(name="active", enumValue="active", displayName="Active"),
            DtdlEnumValue(
                name="inactive", enumValue="inactive", displayName="Inactive"
            ),
            DtdlEnumValue(name="error", enumValue="error", displayName="Error"),
        ],
    )

    # Create an object schema for location
    location_schema = DtdlObjectSchema(
        type="Object",
        displayName="Location",
        fields=[
            DtdlObjectField(name="latitude", schema="double", displayName="Latitude"),
            DtdlObjectField(name="longitude", schema="double", displayName="Longitude"),
            DtdlObjectField(name="altitude", schema="double", displayName="Altitude"),
        ],
    )

    sensor_model = DtdlInterface(
        id="dtmi:com:example:Sensor;1",
        type="Interface",
        context=["dtmi:dtdl:context;3"],
        displayName="Environmental Sensor",
        contents=[
            DtdlProperty(
                name="status",
                schema=status_enum.to_dict(),
                type="Property",
                displayName="Sensor Status",
            ).to_dict(),
            DtdlProperty(
                name="location",
                schema=location_schema.to_dict(),
                type="Property",
                displayName="Sensor Location",
            ).to_dict(),
        ],
    )

    return sensor_model


# Example 3: Creating a model with components
def create_building_model() -> DtdlInterface:
    """Create a Building model that uses components."""

    building_model = DtdlInterface(
        id="dtmi:com:example:Building;1",
        type="Interface",
        context=["dtmi:dtdl:context;3"],
        displayName="Building",
        contents=[
            DtdlProperty(
                name="name",
                schema="string",
                type="Property",
                displayName="Building Name",
            ).to_dict(),
            # Component: HVAC system
            DtdlComponent(
                name="hvacSystem",
                schema="dtmi:com:example:HVACSystem;1",
                type="Component",
                displayName="HVAC System",
            ).to_dict(),
            # Component: Electrical system
            DtdlComponent(
                name="electricalSystem",
                schema="dtmi:com:example:ElectricalSystem;1",
                type="Component",
                displayName="Electrical System",
            ).to_dict(),
            # Relationship: Located in city
            DtdlRelationship(
                name="locatedIn",
                type="Relationship",
                target="dtmi:com:example:City;1",
                displayName="Located In",
                properties=[
                    DtdlProperty(
                        name="address",
                        schema="string",
                        type="Property",
                        displayName="Street Address",
                    )
                ],
            ).to_dict(),
        ],
    )

    return building_model


# Example 4: Parsing a DTDL model from API response
def parse_model_from_api():
    """Retrieve and parse a model from the API."""

    # Get model from API (returns DigitalTwinsModelData)
    model_data = client.get_model(
        "dtmi:com:example:Room;1", include_model_definition=True
    )

    # The model definition is in model_data.model
    # Parse it into a structured DtdlInterface
    if model_data.model:
        dtdl_interface = model_data.model

        print(f"Model ID: {dtdl_interface.id}")
        print(f"Display Name: {dtdl_interface.displayName}")

        if dtdl_interface.contents:
            print(f"Number of contents: {len(dtdl_interface.contents)}")

            # Iterate through contents
            for content in dtdl_interface.contents:
                content_type = content.get("@type", "Unknown")
                content_name = content.get("name", "Unknown")
                print(f"  - {content_type}: {content_name}")

        return dtdl_interface


# Example 5: Creating models in the API
def create_models_in_api():
    """Create DTDL models in the API."""

    # Create models
    room_model = create_room_model()
    sensor_model = create_sensor_model_with_complex_schemas()

    # Convert to dicts for API
    models_to_create = [
        room_model,
        sensor_model,
    ]

    # Create in API
    created_models = client.create_models(models_to_create)

    print(f"Created {len(created_models)} models:")
    for model in created_models:
        print(f"  - {model.id}")

    return created_models


# Example 6: Working with MQTT extensions
def create_model_with_mqtt_extension() -> DtdlInterface:
    """Create a model with MQTT extension properties."""

    mqtt_model = DtdlInterface(
        id="dtmi:com:example:MqttSensor;1",
        type="Interface",
        context=["dtmi:dtdl:context;3"],
        displayName="MQTT Sensor",
        # MQTT extension properties
        telemetryTopic="sensors/{deviceId}/telemetry",
        commandTopic="sensors/{deviceId}/commands",
        payloadFormat="json",
        contents=[
            DtdlTelemetry(
                name="measurement",
                schema="double",
                type="Telemetry",
                displayName="Measurement Value",
            ).to_dict(),
        ],
    )

    return mqtt_model


# Example 7: Model inheritance (extends)
def create_specialized_room_model() -> DtdlInterface:
    """Create a ConferenceRoom that extends the base Room model."""

    conference_room = DtdlInterface(
        id="dtmi:com:example:ConferenceRoom;1",
        type="Interface",
        context=["dtmi:dtdl:context;3"],
        displayName="Conference Room",
        extends="dtmi:com:example:Room;1",  # Inherits from Room
        contents=[
            # Additional properties specific to conference rooms
            DtdlProperty(
                name="capacity",
                schema="integer",
                type="Property",
                displayName="Seating Capacity",
                description="Maximum number of people the room can accommodate",
            ).to_dict(),
            DtdlProperty(
                name="hasProjector",
                schema="boolean",
                type="Property",
                displayName="Has Projector",
            ).to_dict(),
            DtdlProperty(
                name="hasWhiteboard",
                schema="boolean",
                type="Property",
                displayName="Has Whiteboard",
            ).to_dict(),
        ],
    )

    return conference_room


if __name__ == "__main__":
    print("=== DTDL Model Examples ===\n")

    # Example 1: Create structured models
    print("1. Creating Room model...")
    room = create_room_model()
    print(f"   Created: {room.displayName} ({room.id})")
    print(f"   Contents: {len(room.contents or [])} items\n")

    # Example 2: Complex schemas
    print("2. Creating Sensor model with complex schemas...")
    sensor = create_sensor_model_with_complex_schemas()
    print(f"   Created: {sensor.displayName} ({sensor.id})\n")

    # Example 3: Components
    print("3. Creating Building model with components...")
    building = create_building_model()
    print(f"   Created: {building.displayName} ({building.id})\n")

    # Example 4: MQTT extensions
    print("4. Creating MQTT Sensor model...")
    mqtt_sensor = create_model_with_mqtt_extension()
    print(f"   Telemetry Topic: {mqtt_sensor.telemetryTopic}\n")

    # Example 5: Model inheritance
    print("5. Creating Conference Room (extends Room)...")
    conf_room = create_specialized_room_model()
    print(f"   Extends: {conf_room.extends}\n")

    print("✅ All DTDL models created successfully!")
    print("✅ Full type safety for DTDL v3 and v4")
    print("✅ Compatible with FastMCP schema generation")
