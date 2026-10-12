import os
from pypdf import PdfReader

PDF_PATH = "./data/compliance/popia_act_2013.pdf"
OUTPUT_TXT = "./data/compliance/popia_act_text.txt"

def extract_popia_text():
    if not os.path.exists(PDF_PATH):
        print(f"Error: {PDF_PATH} not found.")
        return
    
    print("Extracting text from POPIA PDF...")
    reader = PdfReader(PDF_PATH)
    full_text = ""
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text += f"\n--- PAGE {i+1} ---\n" + text

    os.makedirs(os.path.dirname(OUTPUT_TXT), exist_ok=True)
    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"Successfully extracted {len(reader.pages)} pages to {OUTPUT_TXT}")

if __name__ == "__main__":
    extract_popia_text()
