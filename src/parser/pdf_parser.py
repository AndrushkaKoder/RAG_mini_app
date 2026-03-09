from langchain_community.document_loaders import PyMuPDFLoader
from langchain_qdrant import QdrantVectorStore
import langchain_text_splitters
from langchain_community.embeddings import FastEmbedEmbeddings
import os
import random
import config


class PdfParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.embeddings = FastEmbedEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

        if not os.path.isfile(pdf_path):
            raise FileNotFoundError('PDF файл не загружен для разбора на эмбединги.')

    def parse(self):
        loader = PyMuPDFLoader(self.pdf_path)
        documents = loader.load()

        text_splitter = langchain_text_splitters.RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        chunks = text_splitter.split_documents(documents)

        QdrantVectorStore.from_documents(
            chunks,
            self.embeddings,
            url=config.VECTOR_DB_HOST,
            collection_name=f'my_collection_{random.randint(1, 1000)}',
            force_recreate=False
        )
