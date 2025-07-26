

import re

def split_text_by_lines(text, max_lines=10, overlap=2):
    lines = text.strip().splitlines()

    chunks = []
    i = 0
    while i < len(lines):
        start = i
        end = min(i + max_lines, len(lines))
        chunk = "\n".join(lines[start:end])
        chunks.append(chunk)

        # перекрытие
        i = max(i + max_lines - overlap, start + 1)

    return chunks


def split_text(text, max_words=100, overlap_sentences=1):
    # Если в тексте почти нет пунктуации — fallback на строки
    if len(re.findall(r'[.!?]', text)) < 3:
        return split_text_by_lines(text, max_lines=10, overlap=2)

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
        i = max(i - overlap_sentences, start + 1)
    return chunks
