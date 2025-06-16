# InsightPilot Backend – Upload Module

**Updated:** 2025-06-16



InsightPilot Backend UI + Upload Functionality – Project Summary



Project Name: InsightPilot

Type: Backend Flask API + Frontend UI

Goal: Build a web interface to upload QA files (log, image, video), store them in categorized folders, and eventually process them using your Data Analyst / Data Engineer skills.



Project Initialization

----------------------

- Cloned InsightPilot-backend-flask from GitHub.

- Working under branch: backend/ayesha-api.

- Folder structure:

  InsightPilot-backend-flask/

    ├── app/

    │   ├── __init__.py

    │   ├── routes.py

    │   ├── templates/upload.html

    │   └── utils/storage.py

    ├── static/

    ├── uploads/logs, images, videos

    ├── .env.example

    ├── .gitignore

    ├── requirements.txt

    ├── README.md

    └── run.py



Environment Setup

-----------------

- Virtual environment setup with `python -m venv venv`

- Fixed PowerShell ExecutionPolicy issues.

- Installed Flask, python-dotenv.

- Activated venv and set interpreter in VS Code.



Backend Code Setup

------------------

- run.py runs the app.

- __init__.py registers blueprint.

- routes.py handles upload logic and stores files in correct folders.



Frontend UI Setup

-----------------

- upload.html built with Bootstrap for styling.

- File upload form with dropdown to choose file type.



Functional Testing

------------------

1. Log File Upload: Created sample using echo command.

2. Image Upload: Used sample PNG/JPG.

3. Video Upload: Used test video from sample-videos.com.



Git Status and Sync

-------------------

- Used git add, commit and push to sync changes with branch backend/ayesha-api.



Next Steps

----------

- Add analytics dashboard.

- Store uploaded logs in DB.

- Create visual reports using Power BI.

