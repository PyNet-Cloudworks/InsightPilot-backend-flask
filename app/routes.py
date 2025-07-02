from flask import Blueprint, render_template, request, send_from_directory, redirect
import os
from datetime import datetime
from app.utils.analyser import (
    parse_log_file, vectorize_messages, cluster_messages,
    detect_anomalies, compute_severity_score,
    save_analysis_to_csv, save_summary_report
)

main = Blueprint('main', __name__)

UPLOAD_DIR = 'uploads/logs'
ALLOWED_EXTENSIONS = ['log', 'txt']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def home():
    return redirect('/upload')

@main.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not allowed_file(file.filename):
            return render_template("upload.html", message="❌ Invalid file type.", issues=[])

        filename = datetime.now().strftime('%Y%m%d_%H%M%S_') + file.filename
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        path = os.path.join(UPLOAD_DIR, filename)
        file.save(path)

        df = parse_log_file(path)
        if df.empty:
            return render_template("upload.html", message="✅ File uploaded but no ERROR/WARNING found.", issues=[])

        X = vectorize_messages(df)
        df['cluster'] = cluster_messages(X)
        df['anomaly'] = detect_anomalies(X)
        df['severity_score'] = compute_severity_score(df)

        analysis_path = save_analysis_to_csv(df, filename)
        summary_path = save_summary_report(df, filename)

        return render_template("upload.html",
                               message=f"✅ Analysis complete. {len(df)} issues found.",
                               issues=df.to_dict(orient='records'),
                               report_path=os.path.basename(analysis_path),
                               summary_path=os.path.basename(summary_path),
                               show_download=True)
    return render_template("upload.html", issues=[])

@main.route('/analysis_reports/<path:filename>')
def download_report(filename):
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'analysis_reports'))
    full_path = os.path.join(dir_path, filename)
    if not os.path.exists(full_path):
        return f"File not found: {filename}", 404
    return send_from_directory(dir_path, filename, as_attachment=True)
