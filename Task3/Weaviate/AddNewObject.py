import weaviate
import json
from weaviate.classes.query import Filter

client = weaviate.connect_to_local(
    host="localhost",
    port=8081,
    grpc_port=50051,
)

# Чтение данных из JSON-файла
with open('output.json', 'r', encoding='utf-8') as f:
    entities = json.load(f)

collection = client.collections.get("Test1")

for entity in entities:
    # Маппинг полей из Entity.json в структуру Weaviate
    properties = {
        "label": entity.get("label", ""),
        "abbreviation": entity.get("abbreviation", ""), # строка
        "hasStatement": entity.get("hasStatement", []), # массив строк
        "type": entity.get("type", ""),    
    }
    # properties = {
    #     "prefLabel": entity.get("prefLabel", ""),
    #     "altLabel": entity.get("altLabel", ""),
    #     "abbreviation": entity.get("abbreviation", ""),
    #     "definition": entity.get("definition", ""),
    #     "source": entity.get("source", ""),
    #     "combase": entity.get("combase", ""),
    #     "type": entity.get("type", ""),
    #     "class": entity.get("class", ""),
    #     "comcore": entity.get("comcore", "")       
    # }

    # Проверка существования объекта
    combined_filter = Filter.all_of([
        Filter.by_property("label").equal(properties["label"]),
    ])
    # combined_filter = Filter.all_of([
    #     Filter.by_property("prefLabel").equal(properties["prefLabel"]),
    #     Filter.by_property("definition").equal(properties["definition"]),
    #     Filter.by_property("type").equal(properties["type"])
    # ])

    response = collection.query.fetch_objects(
        limit=1,
        filters=combined_filter
    )

    if len(response.objects) == 0:
        collection.data.insert(properties=properties)
        print(f"Добавлен: {properties['label']}")
    else:
        print(f"Объект '{properties['label']}' уже существует")

# Статистика
current_count = collection.aggregate.over_all(total_count=True).total_count
print(f"\nИтоговое количество объектов: {current_count}")

client.close()