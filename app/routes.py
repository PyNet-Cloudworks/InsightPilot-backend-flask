from flask import Blueprint, render_template, request
import os
import csv
from datetime import datetime
from app.utils.storage import log_task  # ← Import the logger


main = Blueprint('main', __name__)

UPLOAD_DIRS = {
    'log': 'uploads/logs',
    'image': 'uploads/images',
    'video': 'uploads/videos'
}

@main.route('/')  # Home route – this must return the upload UI
def home():
    return render_template('upload.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    filetype = request.form.get('filetype')

    if not file or filetype not in UPLOAD_DIRS:
        log_task(filename="N/A", filetype=filetype or "unknown", status="Failed", message="Invalid file or type")
        return render_template('upload.html', message="Invalid file or file type")

    filename = datetime.now().strftime('%Y%m%d_%H%M%S_') + file.filename
    save_path = os.path.join(UPLOAD_DIRS[filetype], filename)

    os.makedirs(UPLOAD_DIRS[filetype], exist_ok=True)
    file.save(save_path)

    log_task(filename=filename, filetype=filetype, status="Success", message="File uploaded successfully")
    return render_template('upload.html', message=f"{filetype.capitalize()} file uploaded successfully!")

@main.route('/task-logs')
def task_logs():
    logs = []
    log_path = os.path.join("logs", "task_log.csv")
    if os.path.exists(log_path):
        with open(log_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 4:
                    row.append("")  # Add empty message column if missing
                logs.append(row[::-1])  # Reverse to show latest first
    return render_template('task_logs.html', logs=logs)

