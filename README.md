# 🚀 InsightPilot-DSML – Smart Log File Analysis with ML

InsightPilot-DSML is an advanced, lightweight web application built using Flask + Data Science tooling.  
It allows users to upload log files, analyze patterns using machine learning, detect anomalies, cluster similar messages, and generate reports — all with a clean UI.

---

## 🌟 Features

✅ Upload log files (.log, .txt)  
✅ Auto-parse timestamp, level, message  
✅ Clustering of log messages (TF-IDF + KMeans / HDBSCAN)  
✅ Anomaly detection (Isolation Forest)  
✅ Severity scoring (rule-based + ML hybrid)  
✅ Downloadable enriched CSV reports  
✅ Interactive dashboard with error trends (Plotly / Matplotlib)  
✅ REST API for programmatic access  
✅ Minimal UI (Tailwind CSS)

---

## ⚙️ Requirements

- Python 3.10+  
- Flask  
- scikit-learn  
- pandas  
- numpy  
- matplotlib / plotly  
- python-dotenv  
- sentence-transformers (optional)

👉 Install dependencies:

```bash
pip install -r requirements.txt
