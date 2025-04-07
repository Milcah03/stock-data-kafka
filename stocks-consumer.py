import os
from dotenv import load_dotenv
from confluent_kafka import Consumer, KafkaException
from cassandra.cluster import Cluster
from json import loads
from datetime import datetime
import uuid

# --- Load environment variables ---
load_dotenv()

# --- Confluent Kafka Consumer Configuration ---
conf = {
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVER'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv('CONFLUENT_API_KEY'),
    'sasl.password': os.getenv('CONFLUENT_SECRET_KEY'),
    'broker.address.family': 'V4',	
    'group.id': 'stocks-group-id',
    'auto.offset.reset': 'earliest',
}

# Initialize Kafka consumer
consumer = Consumer(conf)
topic = 'stocks-prices'  # Topic name
consumer.subscribe([topic])

# --- Cassandra Setup (Azure Server) ---
try:
    cluster = Cluster(['127.0.0.1'])  # Updated with Azure IP address
    session = cluster.connect()

    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS stocks_data
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
    """)
    session.set_keyspace("stocks_data")

    session.execute("""
        CREATE TABLE IF NOT EXISTS stock_streaming (
            id UUID PRIMARY KEY,
            symbol TEXT,
            opening_price FLOAT,
            closing_price FLOAT,
            date TIMESTAMP
        )
    """)
    print("✅ Cassandra table ready")
except Exception as e:
    print("❌ Error setting up Cassandra:", e)
    session = None

# --- Read from Kafka and Insert into Cassandra ---
if session:
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                try:
                    data = loads(msg.value().decode('utf-8'))

                    # Extract required fields
                    record = {
                       	"id": uuid.uuid4(),
                        "symbol": data.get('T'),
                        "opening_price": data.get('o'),
                        "closing_price": data.get('c'),
                        "date": data.get('t')
		    }
                    # Insert into Cassandra
                    session.execute("""
                        INSERT INTO stock_streaming (id, symbol, opening_price, closing_price, date)
                        VALUES (%(id)s, %(symbol)s, %(opening_price)s, %(closing_price)s, %(date)s)
                   """, record)

                    print(f"✅ Inserted data for {record['symbol']} at {record['date']}")

                except Exception as e:
                    print("❌ Error processing message:", e)

    except KeyboardInterrupt:
        print("🛑 Consumer stopped manually")

    finally:
        consumer.close()
        print("🔒 Kafka consumer closed")
