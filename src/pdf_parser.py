import pathlib

import langchain_text_splitters
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_qdrant import QdrantVectorStore

import src.config
from src.vector_store import clear_storage, get_embeddings


class PdfParser:
    books_dir = 'storage'

    def __init__(self):
        self.embeddings = get_embeddings()

    def parse(self) -> None:
        books = pathlib.Path(self.books_dir).glob("**/*.pdf")

        clear_storage()

        for book in books:
            try:
                print(f'Загрузка файла: {book.name}')

                loader = PyMuPDFLoader(file_path=book)
                documents = loader.load()

                text_splitter = langchain_text_splitters.RecursiveCharacterTextSplitter(
                    chunk_size=800,
                    chunk_overlap=200,
                    separators=["\n\n", "\n", ".", " ", ""]
                )

                chunks = text_splitter.split_documents(documents)

                QdrantVectorStore.from_documents(
                    chunks,
                    self.embeddings,
                    url=src.config.VECTOR_DB_HOST,
                    collection_name=src.config.COLLECT_NAME,
                    force_recreate=False
                )

                print(f'===== Загружен: {book.name} =====')

            except Exception as e:
                print(f'Ошибка загрузки: {str(e)}')
                continue
