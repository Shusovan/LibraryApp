import json
import threading
from kafka import KafkaConsumer

from config.notification import notify_librarian


# Kafka Consumer function that listens for new user registrations.
def consume_kafka():
    
    consumer = KafkaConsumer(
        "user.registered",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        group_id="admin-service-group",
        auto_offset_reset="earliest",
    )

    print("🚀 Listening for user registrations in AdminService...")

    for message in consumer:
        event_data = message.value
        print(f"✅ Received event: {event_data}")

        user_id = event_data.get("user_id")
        email = event_data.get("email")

        if user_id and email:
            print(f"📢 Sending notification for user {user_id} ({email})...")
            notify_librarian(user_id, email)
        else:
            print("⚠️ Missing user_id or email in event data!")

# Run Kafka consumer in a separate thread
kafka_thread = threading.Thread(target=consume_kafka, daemon=True)
kafka_thread.start()

