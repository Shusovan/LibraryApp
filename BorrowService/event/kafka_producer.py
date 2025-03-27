# # Kafka Producer
# import json
# from kafka import KafkaProducer


# producer = KafkaProducer(
#     bootstrap_servers="localhost:9092",
#     value_serializer=lambda v: json.dumps(v).encode("utf-8"),
# )

# def send_event(topic, event_data):
#     """Send an event to Kafka"""
#     producer.send(topic, event_data)
#     producer.flush()