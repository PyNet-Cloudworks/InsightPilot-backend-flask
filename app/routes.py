from flask import Blueprint, render_template, request
import os
import csv
from datetime import datetime
from app.utils.storage import log_task  # ← Import the logger
from .models import UploadLog
from . import db
from app.utils.analyser import analyze_log_file, save_analysis_to_csv
import logging
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
def home():
    return render_template('upload.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    filetype = request.form.get('filetype')

    if not file or filetype not in UPLOAD_DIRS:
        log_task(filename="N/A", filetype=filetype or "unknown", status="Failed", message="Invalid file or type")
        return render_template('upload.html', message="Invalid file or file type")

    # ✅ Validate file extension
    if not allowed_file(file.filename, filetype):
        log_task(filename=file.filename, filetype=filetype, status="Failed", message="File type mismatch")
        return render_template('upload.html', message=f"❌ File extension does not match selected type: {filetype}")

    filename = datetime.now().strftime('%Y%m%d_%H%M%S_') + file.filename
    save_path = os.path.join(UPLOAD_DIRS[filetype], filename)
    os.makedirs(UPLOAD_DIRS[filetype], exist_ok=True)
    file.save(save_path)

    log_task(filename=filename, filetype=filetype, status="Success", message="File uploaded successfully")
    new_log = UploadLog(filename=filename, filetype=filetype)
    db.session.add(new_log)
    db.session.commit()

    if filetype == 'log':
        issues = analyze_log_file(save_path)
        report_filename = filename + '_analysis.csv'
        save_analysis_to_csv(filename, issues)

        report_path = os.path.join("analysis_reports", report_filename)
        if os.path.exists(report_path):
            show_download = True
        else:
            show_download = False

        return render_template('upload.html',
            issues=issues,
            report_path=report_filename,
            show_download=show_download,
            message=f"{filetype.capitalize()} uploaded with {len(issues)} issue(s)."
        )
    
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
                    row.append("")  
                logs.append(row)
        logs = logs[::-1]  # Show latest logs first
    return render_template('task_logs.html', logs=logs)

from flask import send_from_directory
import os

@main.route('/analysis_reports/<path:filename>')
def download_report(filename):
    # Get absolute path to project root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # ../ from app/
    report_dir = os.path.join(base_dir, 'analysis_reports')  # → InsightPilot-backend-flask/analysis_reports
    file_path = os.path.join(report_dir, filename)

    print(f"Looking for file at: {file_path}")

    if not os.path.exists(file_path):
        print("❌ File not found!")
        return f"File not found at: {file_path}", 404

    return send_from_directory(report_dir, filename, as_attachment=True)


