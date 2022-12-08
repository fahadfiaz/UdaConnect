import grpc
import location_pb2
import location_pb2_grpc

"""
Sample of mobile device communicating with gRPC
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:30004")
stub = location_pb2_grpc.LocationServiceStub(channel)

location = location_pb2.LocationMessage(
    person_id=1,
    latitude=-122.2,
    longitude=37.5
)

response = stub.Create(location)
print(f"Response from gRPC server: {response}")
