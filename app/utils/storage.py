import os
from werkzeug.utils import secure_filename
from datetime import datetime

# Define folder paths
UPLOAD_DIRS = {
    'log': 'uploads/logs',
    'image': 'uploads/images',
    'video': 'uploads/videos'
}

# Allowed extensions
EXT_GROUPS = {
    'log': ['.log', '.txt'],
    'image': ['.png', '.jpg', '.jpeg'],
    'video': ['.mp4', '.avi', '.mov']
}

def get_file_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    for type_group, extensions in EXT_GROUPS.items():
        if ext in extensions:
            return type_group
    return None

def save_uploaded_file(file):
    file_type = get_file_type(file.filename)
    if not file_type:
        return None, "Unsupported file type"

    upload_folder = UPLOAD_DIRS[file_type]
    os.makedirs(upload_folder, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = secure_filename(file.filename)
    final_name = f"{timestamp}_{filename}"

    filepath = os.path.join(upload_folder, final_name)
    file.save(filepath)
    return filepath, None
