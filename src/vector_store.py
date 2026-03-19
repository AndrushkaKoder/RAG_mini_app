from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models

import src.config

EMBEDDINGS_MODEL = "intfloat/multilingual-e5-large"


def get_embeddings() -> FastEmbedEmbeddings:
    return FastEmbedEmbeddings(model_name=EMBEDDINGS_MODEL)


def get_vector_store(embeddings: FastEmbedEmbeddings) -> QdrantVectorStore:
    return QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        url=src.config.VECTOR_DB_HOST,
        collection_name=src.config.COLLECT_NAME,
    )


def clear_storage() -> None:
    host = src.config.VECTOR_DB_HOST
    name = src.config.COLLECT_NAME

    client = QdrantClient(url=host)
    if client.collection_exists(collection_name=name):
        print(f"Коллекция {src.config.COLLECT_NAME} удаляется...")
        client.delete_collection(collection_name=name)

        print(f"Создание новой коллекции {src.config.COLLECT_NAME}")
        client.create_collection(
            collection_name=name,
            vectors_config=models.VectorParams(
                size=1024,
                distance=models.Distance.COSINE
            ))
