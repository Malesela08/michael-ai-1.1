import os
import sys

try:
    import yt_dlp
except ImportError:
    print("Installing yt-dlp...")
    os.system(f"{sys.executable} -m pip install yt-dlp")
    import yt_dlp

RIGHT_BRAIN_DIR = "michael_ai/right_brain/datasets"
os.makedirs(RIGHT_BRAIN_DIR, exist_ok=True)

DATASET_URLS = [
    "https://www.youtube.com/watch?v=59HXBFqMca0",  # Lenasia Kidnapping Case Report
    "https://www.youtube.com/watch?v=17Gc-GTpuZY",  # E-Hailing Robbery Caught on Camera
    "https://www.youtube.com/watch?v=6plodohSzUc",  # South African Crime Crisis Documentary
    "https://www.youtube.com/watch?v=h-XQlVcnkSA",  # Disturbing Robberies Caught on Camera
]

ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': os.path.join(RIGHT_BRAIN_DIR, '%(upload_date)s_%(id)s_%(title).50s.%(ext)s'),
    'ignoreerrors': True,
    'nocheckcertificate': True,
}

def download_datasets():
    print("=== Initializing Right Brain Visual Dataset Ingestion ===")
    print(f"Target Directory: {os.path.abspath(RIGHT_BRAIN_DIR)}")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in DATASET_URLS:
            print(f"\n[Ingesting] Processing URL: {url}")
            try:
                ydl.download([url])
                print(f"[Success] Downloaded and mapped to Right Brain: {url}")
            except Exception as e:
                print(f"[Error] Failed to process {url}: {e}")

    print("\n=== Right Brain Ingestion Complete ===")

if __name__ == "__main__":
    download_datasets()
