from huggingface_hub import AsyncInferenceClient

import src.config
from src.vector_store import get_embeddings, get_vector_store


class LLM:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.vector_storage = get_vector_store(self.embeddings)
        self.client = AsyncInferenceClient(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            token=src.config.API_TOKEN,
        )

    async def ask(self, prompt: str) -> str:
        documents = self.vector_storage.similarity_search(k=5, query=prompt)
        context = "\n---\n".join([doc.page_content for doc in documents])

        messages = [
            {
                "role": "system",
                "content": "Ты — опытный библиотекарь. Отвечай кратко и только на основе предоставленного контекста."
            },
            {
                "role": "user",
                "content": f"КОНТЕКСТ:\n{context}\n\nВОПРОС: {prompt}"
            }
        ]

        print("==============")
        print(context)
        print("==============")

        response = await self.client.chat_completion(
            messages=messages,
            max_tokens=500,
            temperature=1,
            top_p=0.5
        )

        return response.choices[0].message.content
