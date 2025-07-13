import weaviate

client = weaviate.connect_to_local(
    host="localhost",
    port=8081,
    grpc_port=50051,
)

collections = client.collections.list_all()
print("Список коллекций:")
for collection in collections:
    print(f"- {collection}")

client.close()