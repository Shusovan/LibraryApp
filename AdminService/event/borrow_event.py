import json
from kafka import KafkaConsumer, KafkaProducer
import requests

# Kafka Consumer for AdminService
consumer = KafkaConsumer(
    "borrow.requested",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    group_id="admin-service-group",
    auto_offset_reset="earliest",
)

# Kafka Producer to send approval response
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def send_event(topic, event_data):
    """Send an event to Kafka"""
    producer.send(topic, event_data)
    producer.flush()

print("🚀 Listening for borrow requests in AdminService...")

for message in consumer:
    event_data = message.value
    user_id = event_data.get("user_id")
    book_id = event_data.get("book_id")

    print(f"📢 Librarian received borrow request for User {user_id}, Book {book_id}")

    # Librarian approval logic (For now, auto-approve)
    approval_status = "APPROVED"

    # Update BorrowService via Kafka
    borrow_response = {
        "user_id": user_id,
        "book_id": book_id,
        "status": approval_status
    }
    send_event("borrow.approved", borrow_response)

    # Notify user
    user_notification = {
        "user_id": user_id,
        "message": f"Your request to borrow book {book_id} has been {approval_status.lower()}."
    }
    send_event("user.notification", user_notification)

    print(f"✅ Borrow request for Book {book_id} is {approval_status}. Notification sent to User {user_id}.")
