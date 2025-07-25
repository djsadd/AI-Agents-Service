'''extract_text(document_file) – извлечь текст из PDF, DOCX, TXT.

split_text(text) – разбить на чанки (например, по 500 токенов).

get_embedding(chunk_text) – вызвать OpenAI или другую модель для создания эмбеддинга.

store_in_quadrant(project_id, chunk_id, vector) – сохранить в Quadrant (или любую векторную БД).

'''
import fitz  # PyMuPDF
from docx import Document
import os


def extract_text(file_path):
    _, ext = os.path.splitext(file_path)

    if ext.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext.lower() == ".docx":
        return extract_text_from_docx(file_path)
    elif ext.lower() == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

import re

def split_text(text, chunk_size=500, overlap=50):
    # Разделим по пробелам на слова (можно заменить на токены позже)
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks

text = "Это очень длинный текст " * 200
chunks = split_text(text)

print(f"Количество чанков: {len(chunks)}")
print(chunks[0][:200])  # Покажи первые 200 символов первого чанка
