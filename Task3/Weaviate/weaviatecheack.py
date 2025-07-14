import weaviate
client = weaviate.connect_to_local(host="localhost", port=8081, grpc_port=50051)
collection = client.collections.get("Test1")
response = collection.query.fetch_objects(limit=10)
for obj in response.objects:
    print(obj.properties)
client.close()