import os
import sys

def climatize_file(file_path, max_chars_per_chunk=10000):
    """
    Prepares and sanity-checks a file before AI ingestion to prevent 
    context window overflows and model crashes.
    """
    if not os.path.exists(file_path):
        print(f"[Error] File not found: {file_path}")
        return None

    file_size = os.path.getsize(file_path)
    print(f"[Prep] Analyzing file: {file_path} ({file_size} bytes)")

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"[Crash Prevention] Failed to read file safely: {e}")
        return None

    # Clean erratic control characters that cause LLM tokenizers to loop or crash
    cleaned_content = "".join(ch for ch in content if ch.printable or ch in "\n\t")

    # If the file is massive, chunk it cleanly to protect local memory
    if len(cleaned_content) > max_chars_per_chunk:
        print(f"[Prep] File is large. Chunking into safe segments...")
        chunks = [cleaned_content[i:i + max_chars_per_chunk] for i in range(0, len(cleaned_content), max_chars_per_chunk)]
        return chunks
    
    return [cleaned_content]
