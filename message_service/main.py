from fastapi import FastAPI
from pydantic import BaseModel
from confluent_kafka import Producer
import json
import datetime

import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import config

app = FastAPI()

class Message(BaseModel):
    sent_at: datetime.datetime
    sender: str
    text: str
    recipient: str

    def __str__(self):
        return self.text

producer = Producer({'bootstrap.servers': config.bootstrap_server})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/messages/")
async def send_message(message: Message):
    message.sent_at = str(message.sent_at)
    # broadcast message to kafka topic
    producer.produce(config.topic, key=message.sent_at, value=json.dumps(message.dict()), callback=delivery_report)
    producer.flush() # flush outstanding messages
    return message
