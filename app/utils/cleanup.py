# utils/cleanup.py
import os, time

def clean_old_files(directory, age_minutes=30):
    now = time.time()
    for root, _, files in os.walk(directory):
        for f in files:
            path = os.path.join(root, f)
            if os.path.isfile(path) and now - os.path.getmtime(path) > age_minutes * 60:
                try:
                    os.remove(path)
                    print(f"🧹 Deleted old file: {path}")
                except Exception as e:
                    print(f"❌ Failed to delete {path}: {e}")

if __name__ == "__main__":
    clean_old_files("uploads")
    clean_old_files("static/processed_images")
    clean_old_files("static/video_frames")
    clean_old_files("analysis_reports")
