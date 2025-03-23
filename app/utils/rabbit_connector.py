import pika
import os

channel = None
connection = None

RABBIT_HOST = os.getenv("RABBIT_HOST")
EXCHANGE = os.getenv("EXCHANGE_NAME")

def init_rabbit():
    global channel, connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST, 5672))
    channel = connection.channel()
    
    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="direct",
        durable=True
    )
    print("Rabbit connected")
    
    
def publish_message(routing_key: str, body):
    channel = get_channel()
    try:
        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2)
        )
    except Exception as e:
        print("Error sending message:", e)
        teardown_rabbit()
        init_rabbit()
        try:
            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=body,
                properties=pika.BasicProperties(delivery_mode=2)
            )
        except Exception as e:
            print("Error on second attempt.")
    
    
def teardown_rabbit():
    global channel, connection
    if channel is not None and channel.is_open:
        channel.close()
        
    if connection and connection.is_open:
        connection.close()
        
def get_channel():
    return channel