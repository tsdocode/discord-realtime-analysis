import sys
import os
import json
from dotenv import load_dotenv
import asyncio
import discord




load_dotenv()



from confluent_kafka import Producer, Consumer

client = discord.Client(intents=discord.Intents.all())
TOKEN = os.getenv('DISCORD_TOKEN')


class KafkaHandler():
    def __init__(self):
        self.__producer_config  = {
            'bootstrap.servers': os.getenv("KAFKA_BROKERS"),
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'SCRAM-SHA-256',
            'sasl.username': os.environ['KAFKA_USERNAME'],
            'sasl.password': os.environ['KAFKA_PASSWORD']
        }

        self.__consumer_config = {
            'bootstrap.servers': os.environ['KAFKA_BROKERS'],
            'group.id': "%s-consumer" % os.environ['KAFKA_USERNAME'],
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'SCRAM-SHA-256',
            'sasl.username': os.environ['KAFKA_USERNAME'],
            'sasl.password': os.environ['KAFKA_PASSWORD']
        }

        self.producer = Producer(self.__producer_config)
        self.consumer = Consumer(self.__consumer_config)

    def produce(self, topic, message):
        self.producer.produce(topic, message)
        self.producer.flush()

    def consume(self, topic, on_message_handler, *args, **kwargs):
        print(topic)
        # client.run(TOKEN)
        self.consumer.subscribe([topic])
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}")
            
            
            print('Received message: {}'.format(msg.value().decode('utf-8')))

            data = json.loads(msg.value().decode('utf-8'))

            on_message_handler(**data)

            



if __name__ == "__main__":
    kafka = KafkaHandler()
    kafka.produce('zfzdjzcz-discord', "Hello message")
    kafka.consume('zfzdjzcz-discord')
