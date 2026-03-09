from fastapi import FastAPI, File, UploadFile
from src.storage import Storage
from parser.pdf_parser import PdfParser

app = FastAPI()

STORAGE_PATH = 'storage'


@app.get("/ask", status_code=200)
async def root(query: str = None) -> dict[str, str]:
    if query is None:
        return {'message': 'Задайте вопрос'}

    ##Будем подцеплять данные из векторной бд и передавать в LLM
    return {"Ваш вопрос": query}


@app.post(path='/api/download', status_code=200)
async def load_file(pdf: UploadFile = File(...)):
    saved_file_path = Storage(pdf).save()

    PdfParser.parse(saved_file_path)

    return {"status": "success", "message": 'Процесс запущен'}
