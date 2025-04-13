import json
from kafka import KafkaConsumer

def consume_kafka():

    # Kafka Consumer for User Notifications
    consumer = KafkaConsumer(
        "user.notification",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        group_id="user-service-group",
        auto_offset_reset="earliest",
    )

    print("🚀 Listening for user notifications in UserService...")

    for message in consumer:
        event_data = message.value
        user_id = event_data.get("user_id")
        message_text = event_data.get("message")

        print(f"📢 Notification for User {user_id}: {message_text}")

    # Here, you can integrate email/SMS notifications.