**📈 Stock Data Extraction using Apache Kafka, Cassandra & Confluent**

This project demonstrates how to extract and stream real-time stock market data using Apache Kafka, process it with Python, and persist it in Apache Cassandra. It leverages Confluent Platform to simplify Kafka setup and management.

**🛠️ Tech Stack**

1. Python

2. Apache Kafka (for real-time data streaming)

3. Confluent Platform (for easier Kafka management)

4. Apache Cassandra (NoSQL database for storing stock data)

5. Kafka-Python (Kafka client library)

6. JSON (data format)

**📌 Project Structure**
```
├── kafka_producer.py        # Sends stock data to Kafka topic
├── kafka_consumer.py        # Consumes stock data and inserts into Cassandra
├── README.md                # Project documentation
```

**🔁 How It Works**

**1. Producer**

Reads data extracted from polygonio

Publishes each record to Kafka topic stock_prices

**2. Kafka (via Confluent Platform)**

Acts as the message broker between producer and consumer

**3. Consumer**

Subscribes to stock_prices topic

Parses stock records and inserts them into Apache Cassandra


**✅ Use Cases**

1. Real-time stock price dashboards

2. Historical stock data warehousing

3. Real-time analytics with Kafka + Cassandra

4. Financial ML model pipelines



