import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pdf_parser import PdfParser


def upload_files_to_vector_db() -> None:
    PdfParser().parse()


upload_files_to_vector_db()
