# app/models.py
from app import db
from datetime import datetime

class UploadLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256))
    filetype = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(64))  # or longer if needed

    def __repr__(self):
        return f"<UploadLog {self.filename}>"
