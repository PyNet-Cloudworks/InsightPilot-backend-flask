from flask import Blueprint, render_template, request, send_from_directory
import os
import csv
import logging
from datetime import datetime

from . import db
from .models import UploadLog
from app.utils.storage import log_task
from app.utils.analyser import analyze_log_file, save_analysis_to_csv
from app.utils.image_processor import annotate_faces_opencv, detect_defects_opencv
from app.utils.image_similarity import check_similarity
from app.utils.video_processor import extract_keyframes

# Setup logging
logging.basicConfig(level=logging.DEBUG)

main = Blueprint('main', __name__)

UPLOAD_DIRS = {
    'log': 'uploads/logs',
    'image': 'uploads/images',
    'video': 'uploads/videos'
}

ALLOWED_EXTENSIONS = {
    'log': ['log', 'txt'],
    'image': ['jpg', 'jpeg', 'png'],
    'video': ['mp4', 'avi', 'mov']
}


# Utility to validate file extension
def allowed_file(filename, filetype):
    ext = filename.lower().rsplit('.', 1)[-1]
    return ext in ALLOWED_EXTENSIONS.get(filetype, [])


# ---------- ROUTES ---------- #

@main.route('/')
def homepage():
    return render_template("index.html", stats={"users": "50M+", "satisfaction": "95%", "insights": "10+"})


@main.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')


@main.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    filetype = request.form.get('filetype')

    if not file or filetype not in UPLOAD_DIRS:
        log_task("N/A", filetype or "unknown", "Failed", "Invalid file or type")
        return render_template('upload.html', message="Invalid file or file type")

    if not allowed_file(file.filename, filetype):
        log_task(file.filename, filetype, "Failed", "File type mismatch")
        return render_template('upload.html', message=f"❌ Extension doesn't match selected type: {filetype}")

    # Save file
    filename = datetime.now().strftime('%Y%m%d_%H%M%S_') + file.filename
    save_dir = UPLOAD_DIRS[filetype]
    save_path = os.path.join(save_dir, filename)
    os.makedirs(save_dir, exist_ok=True)
    file.save(save_path)

    # Log to DB and CSV
    log_task(filename, filetype, "Success", "File uploaded successfully")
    db.session.add(UploadLog(filename=filename, filetype=filetype))
    db.session.commit()

    # --------- LOG FILE ANALYSIS ---------
    if filetype == 'log':
        issues = analyze_log_file(save_path)
        report_filename = filename + '_analysis.csv'
        save_analysis_to_csv(filename, issues)
        report_exists = os.path.exists(os.path.join("analysis_reports", report_filename))
        return render_template('upload.html',
                               message=f"{filetype.capitalize()} uploaded with {len(issues)} issue(s).",
                               issues=issues,
                               report_path=report_filename,
                               show_download=report_exists)

    # --------- IMAGE PROCESSING ---------
    elif filetype == 'image':
        face_img = annotate_faces_opencv(save_path)
        defect_img = detect_defects_opencv(save_path)
        similar_images, _ = check_similarity(save_path)

        return render_template('upload.html',
                               message="✅ Image processed: face & defect detection, similarity check done.",
                               annotated_image=face_img,
                               defect_image=defect_img,
                               similar_images=similar_images)

    # --------- VIDEO PROCESSING ---------
    elif filetype == 'video':
        frames = extract_keyframes(save_path)

        return render_template('upload.html',
            message="🎥 Video uploaded and frames analyzed.",
            video_frames_raw=frames["raw"],
            video_frames_face=frames["face"],
            video_frames_defect=frames["defect"]
        )


    return render_template('upload.html', message=f"{filetype.capitalize()} file uploaded!")


# --------- TASK LOGS VIEW ---------
@main.route('/task-logs')
def task_logs():
    logs = []
    log_path = os.path.join("logs", "task_log.csv")
    if os.path.exists(log_path):
        with open(log_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 4:
                    row.append("")  # Ensure message column
                logs.append(row)
        logs.reverse()  # Latest first
    return render_template('task_logs.html', logs=logs)


# --------- REPORT DOWNLOAD ---------
@main.route('/analysis_reports/<path:filename>')
def download_report(filename):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    report_dir = os.path.join(base_dir, 'analysis_reports')
    file_path = os.path.join(report_dir, filename)

    if not os.path.exists(file_path):
        logging.error(f"❌ Report not found: {file_path}")
        return f"File not found at: {file_path}", 404

    return send_from_directory(report_dir, filename, as_attachment=True)
