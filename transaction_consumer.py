from kafka import KafkaConsumer
import json

# Setup Kafka Consumer
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='fraud-detectors',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🕵️‍♀️ Listening for transactions...\n")

for message in consumer:
    txn = message.value
    print(f"🧾 Received: {txn}")

    # --- Simple fraud rules ---
    if txn["amount"] > 10000:
        print("🚨 High-value transaction flagged!")

    if txn["old_balance"] == 0 and txn["amount"] > 500:
        print("⚠️ Suspicious: No balance but large transaction!")

    if txn["is_fraud"] == 1:
        print("❗ This is an actual fraud case in the dataset.")
    
    print("-" * 50)
