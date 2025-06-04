import pandas as pd
from kafka import KafkaProducer
import json
import time
import os

file_path = os.path.join("data", "transactions.csv")
transactions_df = pd.read_csv(file_path)
transactions_df = transactions_df.sample(500)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Starting to send transactions...")

for idx, row in transactions_df.iterrows():
    
    txn = {
        "txn_id": f"TXN{idx:06}",
        "type": row.get("type", "TRANSFER"),
        "amount": float(row.get("amount", 0)),
        "old_balance": float(row.get("oldbalanceOrg", 0)),
        "new_balance": float(row.get("newbalanceOrig", 0)),
        "is_fraud": int(row.get("isFraud", 0)),
        "timestamp": time.time()
    }
    producer.send("transactions", value=txn)
    print(f"Sent: {txn}")
    time.sleep(1)

producer.flush()