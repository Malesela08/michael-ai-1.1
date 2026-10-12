import urllib.request
import os

POPIA_URL = "https://www.gov.za/sites/default/files/gcis_document/201409/3706726-11act4of2013protectionofpersonalinforcorrect.pdf"
DEST_PATH = "./data/compliance/popia_act_2013.pdf"

def download_popia():
    os.makedirs(os.path.dirname(DEST_PATH), exist_ok=True)
    print("Downloading POPIA Act into Michael AI repository...")
    urllib.request.urlretrieve(POPIA_URL, DEST_PATH)
    print(f"Successfully saved to: {DEST_PATH}")

if __name__ == "__main__":
    download_popia()
