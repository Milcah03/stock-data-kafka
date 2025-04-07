import requests, os, json
from dotenv import load_dotenv
from confluent_kafka import Producer

load_dotenv()

api_key=os.getenv('API_KEY_DATA')
params={
    'adjusted':True,
    'apiKey':api_key
}


url = f'https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2025-04-04'
response=requests.get(url, params=params)
data=response.json()
    

kafka_config={
    'bootstrap.servers':os.getenv('BOOTSTRAP_SERVER'),
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": os.getenv('CONFLUENT_API_KEY'),
    "sasl.password": os.getenv('CONFLUENT_SECRET_KEY'),
    "broker.address.family": "v4",
    "message.send.max.retries": 5,
    "retry.backoff.ms": 500,
}

producer=Producer(kafka_config)
topic='stocks-prices'

for item in data.get('results', []):
    stock_symbol=item.get('T', 'unknown_symbol')
    producer.produce(topic, key=stock_symbol, value=json.dumps(item))
    producer.poll(0)
producer.flush()
