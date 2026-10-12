import os
import sqlite3

TXT_PATH = "./data/compliance/popia_act_text.txt"
DB_PATH = "./data/compliance/popia_rag.db"

def build_popia_index():
    if not os.path.exists(TXT_PATH):
        print(f"Error: {TXT_PATH} not found.")
        return

    print("Reading extracted POPIA text...")
    with open(TXT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by the exact header generated during extraction
    raw_pages = content.split("--- PAGE ")
    
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS popia_docs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_num TEXT,
            content TEXT
        );
    """)

    indexed_count = 0
    for block in raw_pages:
        if not block.strip():
            continue
        
        # Extract page number and text body
        lines = block.strip().split("\n")
        header = lines[0] # e.g. "1 ---"
        page_num = header.split("---")[0].strip()
        page_text = "\n".join(lines[1:]).strip()
        
        if page_text:
            cursor.execute("INSERT INTO popia_docs (page_num, content) VALUES (?, ?);", (page_num, page_text))
            indexed_count += 1

    conn.commit()
    conn.close()
    print(f"Successfully indexed {indexed_count} pages into {DB_PATH}!")

if __name__ == "__main__":
    build_popia_index()
