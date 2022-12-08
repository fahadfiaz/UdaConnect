from kafka import KafkaConsumer
import os
import json
import psycopg2

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

kafka_topic = "location"
kafka_url = 'my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092'
consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_url)


def save_location(location):
    connection = psycopg2.connect(
        dbname=DB_NAME,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
    )

    with connection.cursor() as cursor:
        try:
            query = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}));".format(
                int(location["person_id"]),
                float(location["latitude"]),
                float(location["longitude"]),
            )
            cursor.execute(query)
            print(f"Location of a person with id : {int(location['person_id'])} saved")
        except Exception as error:
            print(f"Exception : {error}")


for message in consumer:
    decoded_message = message.value.decode("utf-8")
    location = json.loads(decoded_message)
    save_location(location)
