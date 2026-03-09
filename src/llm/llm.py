import config
import ollama


class LLM:
    def __init__(self):
        self.model = config.LLM_NAME
        self.host = config.LLM_HOST
        self.client = ollama.AsyncClient(self.host)

    async def send(self, prompt: str) -> str:
        response = await self.client.chat(
            model=self.model,
            messages=[
                {'role': 'system', 'content': self.get_system_prompt()},
                {'role': 'user', 'content': prompt},
            ],
            options={
                "temperature": 0.0,
                "num_ctx": 8192,
            },
        )

        return response['message']['content']

    @staticmethod
    def get_system_prompt() -> str:
        return (
            "Ты — строгий корпоративный ассистент компании. "
            "Твое правило:\n"
            "Если в запросе есть нецензурная брань, оскорбления или вызывающе неделовой стиль — "
            "сразу отвечай: 'Я придерживаюсь делового стиля общения и не могу ответить на такой запрос.' и прекращай диалог.\n"
        )
