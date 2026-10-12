import sqlite3
import sys

DB_PATH = "./data/compliance/popia_rag.db"

def search_popia(query_term):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    sql_query = """
        SELECT page_num, content 
        FROM popia_docs 
        WHERE content LIKE ? 
        LIMIT 3;
    """
    cursor.execute(sql_query, (f"%{query_term}%",))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print(f"\nNo results found for query: '{query_term}'")
        return

    print(f"\n=== POPIA Search Results for '{query_term}' ===")
    for page_num, snippet in results:
        print(f"\n[ PAGE {page_num} ]")
        clean_snippet = " ".join(snippet.split())
        print(clean_snippet[:350] + "...\n" + "-"*40)

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "condition"
    search_popia(query)
