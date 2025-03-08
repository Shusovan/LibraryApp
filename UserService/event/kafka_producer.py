import json
import uuid
from kafka import KafkaProducer


# Custom JSON serializer to handle UUIDs
def json_serializer(obj):
    
    if isinstance(obj, uuid.UUID):
        return str(obj)  # Convert UUID to string
    
    raise TypeError(f"Type {type(obj)} is not serializable")


# Kafka Producer with the custom serializer
producer = KafkaProducer(bootstrap_servers="localhost:9092",value_serializer=lambda v: json.dumps(v, default=json_serializer).encode("utf-8"),)


def send_event(topic, event_data):
    producer.send(topic, event_data)
    producer.flush()


# Call this function when a user registers
def user_registered_event(id: uuid.UUID, email: str):
    event_data = {"id": str(id), "email": email, "status": "PENDING"}
    send_event("user.registered", event_data)