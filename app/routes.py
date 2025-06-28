from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for, session
import os
import logging
from datetime import datetime
from . import db
from .models import UploadLog
from app.utils.analyser import analyze_log_file, save_analysis_to_csv
from app.utils.image_processor import annotate_faces_opencv, detect_defects_opencv
from app.utils.image_similarity import check_similarity
from app.utils.video_processor import extract_keyframes

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

def allowed_file(filename, filetype):
    ext = filename.lower().rsplit('.', 1)[-1]
    return ext in ALLOWED_EXTENSIONS.get(filetype, [])

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
        return render_template('upload.html', message="Invalid file or file type")

    if not allowed_file(file.filename, filetype):
        return render_template('upload.html', message=f"❌ Extension doesn't match selected type: {filetype}")

    filename = datetime.now().strftime('%Y%m%d_%H%M%S_') + file.filename
    save_dir = UPLOAD_DIRS[filetype]
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    file.save(save_path)

    # Save to database only (not CSV)
    if 'session_id' not in session:
        session['session_id'] = os.urandom(8).hex()

    upload_log = UploadLog(
        filename=filename,
        filetype=filetype,
        session_id=session['session_id']
    )
    db.session.add(upload_log)
    db.session.commit()

    if filetype == 'log':
        issues = analyze_log_file(save_path)
        report_filename = filename + '_analysis.csv'
        save_analysis_to_csv(filename, issues)
        report_path = os.path.join("analysis_reports", report_filename)
        return render_template('upload.html',
                               message=f"{filetype.capitalize()} uploaded with {len(issues)} issue(s).",
                               issues=issues,
                               report_path=report_filename,
                               show_download=os.path.exists(report_path))

    elif filetype == 'image':
        face_img = annotate_faces_opencv(save_path)
        defect_img = detect_defects_opencv(save_path)
        similar_images, _ = check_similarity(save_path)
        return render_template('upload.html',
                               message="✅ Image processed.",
                               annotated_image=face_img,
                               defect_image=defect_img,
                               similar_images=similar_images)

    elif filetype == 'video':
        frames = extract_keyframes(save_path)
        return render_template('upload.html',
                               message="🎥 Video uploaded and frames analyzed.",
                               video_frames_raw=frames["raw"],
                               video_frames_face=frames["face"],
                               video_frames_defect=frames["defect"])

    return render_template('upload.html', message="Upload complete.")

@main.route('/analysis_reports/<path:filename>')
def download_report(filename):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    report_dir = os.path.join(base_dir, 'analysis_reports')
    file_path = os.path.join(report_dir, filename)

    if not os.path.exists(file_path):
        return f"File not found at: {file_path}", 404

    return send_from_directory(report_dir, filename, as_attachment=True)

@main.route('/my-uploads')
def my_uploads():
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('main.upload_page'))

    uploads = UploadLog.query.filter_by(session_id=session_id).order_by(UploadLog.timestamp.desc()).all()
    return render_template('upload.html', my_uploads=uploads)

@main.route('/clear-uploads')
def clear_uploads():
    session_id = session.get('session_id')
    if session_id:
        UploadLog.query.filter_by(session_id=session_id).delete()
        db.session.commit()
    return redirect(url_for('main.upload_page'))
