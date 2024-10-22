from kafka import KafkaConsumer
import json

def json_deserializer(data):
    return json.loads(data.decode('utf-8'))

consumer = KafkaConsumer(
    'reaction',
    bootstrap_servers=['broker-1:9092', 'broker-2:9092', 'broker-3:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=json_deserializer
)

for message in consumer:
    print(f"Received message: {message.value}")
