from kafka import KafkaConsumer
import json
import pandas as pd
import os

# Prepare log file
log_file = "fraud_log.csv"

# If file doesn't exist, create with headers
if not os.path.exists(log_file):
    pd.DataFrame(columns=["txn_id", "type", "amount", "sender", "reason"]).to_csv(log_file, index=False)

# Kafka consumer setup
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='fraud-detectors',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🕵️ Listening for suspicious transactions...\n")

for message in consumer:
    txn = message.value
    print(f"Received: {txn}")

    # Simple fraud rules
    flagged = False
    reason = ""

    if txn["amount"] > 10000:
        flagged = True
        reason = "Amount exceeds $10,000"

    elif txn["old_balance"] == 0 and txn["amount"] > 500:
        flagged = True
        reason = "High transaction from zero balance"

    elif txn["is_fraud"] == 1:
        flagged = True
        reason = "Labelled as fraud in dataset"

    if flagged:
        # Append to fraud_log.csv
        log_df = pd.DataFrame([{
            "txn_id": txn["txn_id"],
            "type": txn["type"],
            "amount": txn["amount"],
            # "sender": txn["sender"],
            "reason": reason
        }])
        log_df.to_csv(log_file, mode='a', header=False, index=False)
        print(f"🚨 Fraud detected: {txn['txn_id']} - {reason}")

    print("-" * 50)
