import weaviate
from weaviate.classes.query import MetadataQuery
import json
import os
import re

try:
    os.mkdir("Test_NewOntology")
except:
    OUTPUT_DIR = "Test_NewOntology"

    with open("NeedEntity.json", "r", encoding="utf-8") as f:
        test_entity = json.load(f)

    client = weaviate.connect_to_local(
        host="localhost",
        port=8081,
        grpc_port=50051,
    )

    collection = client.collections.get("Test1")

    for i, entity in enumerate(test_entity):
        statements_str = " ".join(entity["hasStatement"]) if entity["hasStatement"] else ""
        
        query_parts = [
            entity["label"],
            entity["abbreviation"],
        ]
        query_text = " ".join(filter(None, query_parts))
        
        class_filter = weaviate.classes.query.Filter.by_property("type").equal(entity["type"])
        
        response = collection.query.hybrid(
            query=query_text,
            alpha=0.4,
            query_properties=["label", "abbreviation"],
            filters=class_filter,
            return_metadata=MetadataQuery(score=True, explain_score=True),
            limit=8
        )
        
        safe_label = re.sub(r'[\\/*?:"<>|]', "", entity["label"])
        filename = f"{safe_label[:50]}.json"
        full_path = os.path.join(OUTPUT_DIR, filename)
        
        # Сохраняем только результаты с score > 0.5
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(
                [
                    {
                        "properties": obj.properties,
                        "metadata": {
                            "score": obj.metadata.score,
                            "explain_score": obj.metadata.explain_score
                        }
                    }
                    for obj in response.objects if obj.metadata.score > 0.5
                ],
                f,
                ensure_ascii=False,
                indent=2
            )

    client.close()