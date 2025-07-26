from services.utils.extract import extract_text
from services.utils.splitter import split_text
from services.embeddings.encode import get_embeddings
from services.qdrant.uploader import (upload_to_qdrant)

TEST_FILE_PATH = r"C:\Users\admin\PycharmProjects\AI-Agent\AISERVICE\tests files\test.docx"


def test_pipeline():
    print("🔍 Тестируем pipeline на файле:", TEST_FILE_PATH)

    text = extract_text(TEST_FILE_PATH)
    chunks = split_text(text)
    embeddings = get_embeddings(chunks)
    upload_to_qdrant(embeddings, chunks, file_id="test_file_for_pipeline")


if __name__ == "__main__":
    test_pipeline()
