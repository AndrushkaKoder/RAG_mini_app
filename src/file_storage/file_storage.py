import shutil
from fastapi import UploadFile, File
import pathlib

class FileStorage:
    storage_path = 'storage'

    def __init__(self, file: UploadFile = File(...)):
        self.file = file
        self.filepath = f'{self.storage_path}/{file.filename}'

    def make_dir(self) -> None:
        path = pathlib.Path(self.storage_path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

    def save(self):
        self.make_dir()

        with open(self.filepath, "wb") as buffer:
            shutil.copyfileobj(self.file.file, buffer)

        return self.filepath
