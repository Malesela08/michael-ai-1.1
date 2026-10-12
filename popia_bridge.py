import sqlite3
import os

DB_PATH = "./data/compliance/popia_rag.db"

def query_popia(topic: str, max_results: int = 2) -> list:
    """
    Queries the local POPIA database for compliance requirements 
    relevant to a specific topic, data type, or security action.
    """
    if not os.path.exists(DB_PATH):
        return ["Error: POPIA compliance database not found."]
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT page_num, content 
        FROM popia_docs 
        WHERE content LIKE ? 
        LIMIT ?;
    """, (f"%{topic}%", max_results))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return [f"No specific statutory clauses found for topic: '{topic}'."]
        
    compliance_rules = []
    for page_num, snippet in results:
        clean_text = " ".join(snippet.split())
        compliance_rules.append(f"[POPIA Statute - Page {page_num}]: {clean_text[:300]}...")
        
    return compliance_rules

if __name__ == "__main__":
    # Test the bridge
    print("Testing POPIA Agent Bridge...")
    rules = query_popia("biometrics")
    for r in rules:
        print(r)
