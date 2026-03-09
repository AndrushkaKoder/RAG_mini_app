from typing import Any
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from pydantic import BaseModel
from src.pdf_parser.pdf_parser import PdfParser
from src.llm.llm import LLM

app = FastAPI()


class AskRequest(BaseModel):
    prompt: str


@app.post("/api/query", status_code=200)
async def query(request: AskRequest) -> dict[str, Any] | None:
    prompt = request.prompt
    model = LLM()
    response = await model.ask(prompt)

    return {'response': response}


@app.post(path='/api/upload', status_code=200)
async def load_file(file: UploadFile = File(...)):
    pass


@app.get('/api/index', status_code=200)
async def index(tasks: BackgroundTasks):
    parser = PdfParser()

    tasks.add_task(func=parser.parse)

    return {'message': 'ok'}
