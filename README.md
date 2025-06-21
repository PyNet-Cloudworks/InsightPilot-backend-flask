# 📤 InsightPilot – QA File Upload and Log Analysis

InsightPilot is a Flask-based tool for uploading QA files, analyzing `.log` files for errors/warnings, and tracking uploads in CSV and PostgreSQL (via pgAdmin).

---

## ✅ Features

- Upload and parse `.log` files for issues.
- Downloadable `.csv` reports generated per upload.
- Upload logging to both local CSV and PostgreSQL.
- Web UI built using Bootstrap 5.
- pgAdmin used to inspect and manage backend DB logs.

---

## 🛠️ Tech Stack

- **Python** (Flask, SQLAlchemy)
- **PostgreSQL + pgAdmin**
- **HTML + Bootstrap**
- **dotenv + YAML config**

---

## 🗃️ Folder Structure

InsightPilot-backend-flask/
│
├── app/
│ ├── routes.py
│ ├── models.py
│ ├── init.py
│ └── utils/
│ ├── analyser.py
│ └── storage.py
│
├── analysis_reports/ # Generated CSVs
├── logs/ # Upload log CSV
├── uploads/ # Uploaded files
├── static/ # Styles
├── templates/ # HTML templates
│ ├── upload.html
│ └── task_logs.html
│
├── instance/ # Flask config (optional)
├── .env # Environment variables
├── .env.example # Template
├── insightpilot_config.yaml # 🔧 YAML-based config
├── requirements.txt # Dependencies (frozen)
├── run.py # Entry point
└── README.md