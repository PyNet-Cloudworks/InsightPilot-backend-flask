from flask import Blueprint, render_template, request, send_from_directory
import os
import csv
from datetime import datetime
import logging

from .models import UploadLog
from . import db
from app.utils.storage import log_task
from app.utils.analyser import analyze_log_file, save_analysis_to_csv
from app.utils.image_processor import annotate_faces_opencv
from app.utils.image_similarity import check_similarity

# Logging setup
logging.basicConfig(level=logging.DEBUG)

main = Blueprint('main', __name__)

UPLOAD_DIRS = {
    'log': 'uploads/logs',
    'image': 'uploads/images',
    'video': 'uploads/videos'
}

def allowed_file(filename, filetype):
    ext = filename.lower().rsplit('.', 1)[-1]
    allowed_extensions = {
        'log': ['log', 'txt'],
        'image': ['jpg', 'jpeg', 'png'],
        'video': ['mp4', 'avi', 'mov']
    }
    return ext in allowed_extensions.get(filetype, [])

@main.route('/')
def homepage():
    return render_template("index.html", stats={"users": "50M+", "satisfaction": "95%", "insights": "10+"})

@main.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

# --- Upload Handler ---
@main.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    filetype = request.form.get('filetype')

    if not file or filetype not in UPLOAD_DIRS:
        log_task(filename="N/A", filetype=filetype or "unknown", status="Failed", message="Invalid file or type")
        return render_template('upload.html', message="Invalid file or file type")

    if not allowed_file(file.filename, filetype):
        log_task(filename=file.filename, filetype=filetype, status="Failed", message="File type mismatch")
        return render_template('upload.html', message=f"❌ File extension does not match selected type: {filetype}")

    # Save the file
    filename = datetime.now().strftime('%Y%m%d_%H%M%S_') + file.filename
    save_path = os.path.join(UPLOAD_DIRS[filetype], filename)
    os.makedirs(UPLOAD_DIRS[filetype], exist_ok=True)
    file.save(save_path)

    log_task(filename=filename, filetype=filetype, status="Success", message="File uploaded successfully")
    db.session.add(UploadLog(filename=filename, filetype=filetype))
    db.session.commit()

    # --- Log Analysis ---
    if filetype == 'log':
        issues = analyze_log_file(save_path)
        report_filename = filename + '_analysis.csv'
        save_analysis_to_csv(filename, issues)
        report_path = os.path.join("analysis_reports", report_filename)
        show_download = os.path.exists(report_path)
        return render_template('upload.html', issues=issues, report_path=report_filename, show_download=show_download,
                               message=f"{filetype.capitalize()} uploaded with {len(issues)} issue(s).")

    # --- Image Annotation & Similarity ---
    if filetype == 'image':
        annotated_filename = annotate_faces_opencv(save_path)
        similar_images, new_hash = check_similarity(save_path)
        return render_template('upload.html',
                               message="✅ Image uploaded, annotated, and checked for duplicates.",
                               annotated_image=annotated_filename,
                               similar_images=similar_images)

    return render_template('upload.html', message=f"{filetype.capitalize()} file uploaded successfully!")

# --- Task Log Viewer ---
@main.route('/task-logs')
def task_logs():
    logs = []
    log_path = os.path.join("logs", "task_log.csv")
    if os.path.exists(log_path):
        with open(log_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 4:
                    row.append("")  # Padding if needed
                logs.append(row)
        logs.reverse()
    return render_template('task_logs.html', logs=logs)

# --- Report Downloader ---
@main.route('/analysis_reports/<path:filename>')
def download_report(filename):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    report_dir = os.path.join(base_dir, 'analysis_reports')
    file_path = os.path.join(report_dir, filename)

    if not os.path.exists(file_path):
        logging.error(f"❌ File not found at: {file_path}")
        return f"File not found at: {file_path}", 404

    return send_from_directory(report_dir, filename, as_attachment=True)
