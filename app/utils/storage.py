# import os
# from werkzeug.utils import secure_filename
# from datetime import datetime

# # Define folder paths
# UPLOAD_DIRS = {
#     'log': 'uploads/logs',
#     'image': 'uploads/images',
#     'video': 'uploads/videos'
# }

# # Allowed extensions
# EXT_GROUPS = {
#     'log': ['.log', '.txt'],
#     'image': ['.png', '.jpg', '.jpeg'],
#     'video': ['.mp4', '.avi', '.mov']
# }

# def get_file_type(filename):
#     ext = os.path.splitext(filename)[1].lower()
#     for type_group, extensions in EXT_GROUPS.items():
#         if ext in extensions:
#             return type_group
#     return None

# def save_uploaded_file(file):
#     file_type = get_file_type(file.filename)
#     if not file_type:
#         return None, "Unsupported file type"

#     upload_folder = UPLOAD_DIRS[file_type]
#     os.makedirs(upload_folder, exist_ok=True)

#     timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#     filename = secure_filename(file.filename)
#     final_name = f"{timestamp}_{filename}"

#     filepath = os.path.join(upload_folder, final_name)
#     file.save(filepath)
#     return filepath, None

import os
import csv
from datetime import datetime

def log_task(filename, filetype, status, message=""):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # This should create the folder if missing
    log_file = os.path.join(log_dir, "task_log.csv")

    with open(log_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename, filetype, status, message])

