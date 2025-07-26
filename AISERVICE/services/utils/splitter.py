import re


def split_text(text, max_words=100, overlap_sentences=1):
    # Разбиваем текст на предложения
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    chunks = []
    current_chunk = []
    current_length = 0

    i = 0
    while i < len(sentences):
        current_chunk = []
        current_length = 0
        start = i

        while i < len(sentences) and current_length + len(sentences[i].split()) <= max_words:
            current_chunk.append(sentences[i])
            current_length += len(sentences[i].split())
            i += 1

        chunks.append(" ".join(current_chunk))

        # Смещаемся назад для перекрытия (на `overlap_sentences` предложений)
        i = max(i - overlap_sentences, start + 1)

    return chunks
