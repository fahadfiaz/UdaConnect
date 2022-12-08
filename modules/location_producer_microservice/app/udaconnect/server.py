import grpc
import json
import location_pb2
import location_pb2_grpc
from concurrent import futures
from kafka import KafkaProducer

kafka_topic = "location"
kafka_url = 'my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092'
producer = KafkaProducer(bootstrap_servers=kafka_url)


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        location = {
            "person_id": request.person_id,
            "latitude": request.latitude,
            "longitude": request.longitude,
        }

        location_encoded = json.dumps(location).encode('utf-8')
        producer.send(kafka_topic, location_encoded)
        producer.flush()

        return location_pb2.LocationMessage(**location)


# Initializes the gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)
server.add_insecure_port("[::]:5005")
server.start()
print("server started")
server.wait_for_termination()