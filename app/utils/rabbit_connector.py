import pika
import os

import pika.credentials

RABBIT_HOST = os.getenv("RABBIT_HOST")
EXCHANGE = os.getenv("EXCHANGE_NAME")

# def init_rabbit():
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST, 5672))
channel = connection.channel()

channel.exchange_declare(
    exchange=EXCHANGE,
    exchange_type="direct",
    durable=True
)
print("Rabbit connected")
    
    
def teardown_rabbit():
    if channel:
        channel.close()
        
    if connection and connection.is_open:
        connection.close()