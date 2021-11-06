# kafka consumer subscribes to the message_topic
# retrieves the messages
# transforms the messages
# loads the messages into a database

import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from config import *
from utils.utils import init_postgres_conn

from confluent_kafka import Consumer, KafkaException
from psycopg2.sql import SQL, Identifier
import ast

def main():
    consumer = Consumer({'bootstrap.servers': bootstrap_server, 'group.id': 'message_service', 'auto.offset.reset': 'earliest'})
    consumer.subscribe([topic])

    # create a postgres connection
    conn = init_postgres_conn(
        postgres_host,
        postgres_port,
        postgres_database,
        postgres_user,
        postgres_password,
    )
    cur = conn.cursor() # create a cursor    

    # Read messages from Kafka, do some simple cleaning and write to postgres
    try:
        while True:
            msg = consumer.poll(timeout=1.0) # poll for messages from the topic
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                # Proper message
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                    (msg.topic(), msg.partition(), msg.offset(),
                                    str(msg.key())))
                print(msg.value()) # is of bytes type

                msg_value = msg.value().decode('utf-8')
                # etl here
                msg_dict = ast.literal_eval(msg_value) # convert the string representation of the dict into an actual python dict
                # just for the sake of some simple transformation, clean the timestamp a little bit - we only need the time up to the seconds granularity
                msg_dict['sent_at'] = msg_dict['sent_at'].split('.')[0]
                # run the sql query to insert the message into postgres
                cur.execute(
                    SQL("INSERT INTO {} (sent_at, sender, text, recipient) VALUES (%s, %s, %s, %s)")
                    .format(Identifier('messages')),
                    [msg_dict['sent_at'], msg_dict['sender'], msg_dict['text'], msg_dict['recipient']])
                conn.commit()

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()
        conn.close() # close postgres connection when not listening to messages in kafka anymore

if __name__ == "__main__":
    main()