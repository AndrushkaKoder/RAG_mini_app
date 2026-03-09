import ollama
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import FastEmbedEmbeddings
import src.config


class LLM:
    def __init__(self):
        self.model = src.config.LLM_NAME
        self.host = src.config.LLM_HOST
        self.client = ollama.AsyncClient(self.host)
        self.embeddings = FastEmbedEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.vector_storage = QdrantVectorStore.from_existing_collection(
            embedding=self.embeddings,
            url=src.config.VECTOR_DB_HOST,
            collection_name=src.config.COLLECT_NAME,
        )

    async def ask(self, prompt: str) -> str:
        documents = self.vector_storage.similarity_search(k=8, query=prompt)

        context = ''
        for document in documents:
            context += "\n\n---\n\n" + document.page_content

        full_prompt = f"КОНТЕКСТ:\n{context}\n\nВОПРОС: {prompt}"

        print("======" + '\n' + '======' + '\n' + full_prompt )
        response = await self.client.chat(
            model=self.model,
            messages=[
                {'role': 'system', 'content': self.get_system_prompt()},
                {'role': 'user', 'content': full_prompt},
            ],
            options={
                "temperature": 0.1,
                "num_ctx": 8192,
            },
        )

        return response['message']['content']

    @staticmethod
    def get_system_prompt() -> str:
        return (
            "Ты — помощник-библиотекарь. Используй только предоставленный текст (контекст), "
            "чтобы ответить на вопрос пользователя. Если в тексте нет ответа, так и скажи. "
            "Отвечай вежливо и по делу."
        )
