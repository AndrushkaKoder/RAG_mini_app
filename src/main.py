from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from src.llm import LLM


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = LLM()
    yield


app = FastAPI(lifespan=lifespan)


class AskRequest(BaseModel):
    prompt: str


@app.post("/api/query", status_code=200)
async def query(request: AskRequest) -> dict[str, Any] | None:
    response = await app.state.model.ask(request.prompt)
    return {"response": response}
