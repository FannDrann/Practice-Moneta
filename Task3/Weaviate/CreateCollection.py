import weaviate
from weaviate.classes.config import Configure, Tokenization
import weaviate.classes as wvc

# Стандартный порт для подключения к БД, это 8080. Но так как в docker-compose мы указали свободные порт 8081, то необходимо принудительно передать аргумент
client = weaviate.connect_to_local(
    host="localhost",
    port=8081,
    grpc_port=50051,
)
try:
    client.collections.delete("Test1")
    # Здесь создаём БД (коллекцию), перечисляем необходимые нам атрибуты у сущности
    collection = client.collections.create(
        name="Test1", # название коллекции
        properties=[
            wvc.config.Property(
                name="label", # имя атрибута
                data_type=wvc.config.DataType.TEXT, # тип данных атрибута
                vectorize_property_name=True,# векторизовать этот атрибут? (True/False)
                tokenization=Tokenization.LOWERCASE, # токенизация происходит под нижним регистром "Папа -> папа"
                index_filterable=True, # фильтрация для инвертированного индекса? (True/False)
                index_searchable=True, # поиск для инвертированного индекса? (True/False)
            ),
            wvc.config.Property(
                name="abbreviation",
                data_type=wvc.config.DataType.TEXT,
                vectorize_property_name=True,
                tokenization=Tokenization.LOWERCASE,
                index_filterable=True,
                index_searchable=True,
            ),
            wvc.config.Property(
                name="hasStatement",
                data_type=wvc.config.DataType.TEXT_ARRAY,
                vectorize_property_name=True,
                tokenization=Tokenization.LOWERCASE,
                index_filterable=True,
                index_searchable=True,
            ),
            wvc.config.Property(
                name="type",
                data_type=wvc.config.DataType.TEXT,
                skip_vectorization=True, # пропускаем векторизацию? (True/False) этот атрибут только используется для фильтрации
            ),
        ],
        # vectorizer_config=Configure.Vectorizer.text2vec_transformers(
        #     model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        # )
    )
finally:
    print('Collection created')
    client.close()
