from flask import Blueprint, render_template, request
import os
from datetime import datetime

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
        return render_template('upload.html', message="Invalid file or file type")

    filename = datetime.now().strftime('%Y%m%d_%H%M%S_') + file.filename
    save_path = os.path.join(UPLOAD_DIRS[filetype], filename)

    os.makedirs(UPLOAD_DIRS[filetype], exist_ok=True)
    file.save(save_path)

    return render_template('upload.html', message=f"{filetype.capitalize()} file uploaded successfully!")
