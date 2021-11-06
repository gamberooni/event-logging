## Introduction
This is a proof-of-concept of how to emit events from within a web service as a publisher to a message queue service, and a subscriber listens to the particular message queue topic for the messages, performs some simple data cleaning, and finally writes the cleaned data to a database.

- Web service - FastAPI
- Message queue - Kafka
- Publisher - Kafka client within FastAPI
- Subscriber - Kafka client
- Database - PostgreSQL

## Setup Steps
1. git clone this repo
2. cd event-logging
3. pip install -r requirements.txt
4. Start Kafka and PostgreSQL by running `docker-compose up -d`
5. cd message_service
6. Create Kafka topic by running `python utils/create_topic.py`
7. Initialize the database table schema by running `python utils/create_db_schema.py`
8. Start the FastAPI server by running `uvicorn main:app --reload`
9. Start the Kafka subscriber that listens to the Kafka topic and performs some simple ETL to the Postgres by running `python etl/etl.py`
10. Start the web server client application which generates fake messages by calling POST request to the FastAPI web server by running `python client.py`

## Cleanup 
- docker-compose down
- Hit `Ctrl + C` on the all scripts that you run in the terminals