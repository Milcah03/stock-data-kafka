📈 Stock Data Extraction using Apache Kafka, Cassandra & Confluent
This project demonstrates how to extract and stream real-time stock market data using Apache Kafka, process it with Python, and persist it in Apache Cassandra. It leverages Confluent Platform to simplify Kafka setup and management.

🛠️ Tech Stack
Python

Apache Kafka (for real-time data streaming)

Confluent Platform (for easier Kafka management)

Apache Cassandra (NoSQL database for storing stock data)

Kafka-Python (Kafka client library)

JSON (data format)

📌 Project Structure
├── kafka_producer.py        # Sends stock data to Kafka topic
├── kafka_consumer.py        # Consumes stock data and inserts into Cassandra
├── README.md                # Project documentation


🔁 How It Works
Producer

Reads data extracted from polygonio

Publishes each record to Kafka topic stock_prices

Kafka (via Confluent Platform)

Acts as the message broker between producer and consumer

Consumer

Subscribes to stock_prices topic

Parses stock records and inserts them into Apache Cassandra


✅ Use Cases
Real-time stock price dashboards

Historical stock data warehousing

Real-time analytics with Kafka + Cassandra

Financial ML model pipelines

🙌 Credits
Project by Milcah03, based on the tutorial Stock Data Extraction using Apache Kafka.

