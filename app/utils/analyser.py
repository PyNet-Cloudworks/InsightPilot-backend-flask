import re
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

def parse_log_file(filepath):
    pattern = re.compile(r"\[(.*?)\]\s+(ERROR|WARNING)\s+(.*)")
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                ts, level, msg = match.groups()
                records.append({'timestamp': ts, 'level': level, 'message': msg})
    return pd.DataFrame(records)

def vectorize_messages(df):
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    return vectorizer.fit_transform(df['message'])

def cluster_messages(X):
    n = X.shape[0]
    if n < 1:
        return []
    if n == 1:
        return [0]
    kmeans = KMeans(n_clusters=min(3, n), random_state=42, n_init=10)
    return kmeans.fit_predict(X)

def detect_anomalies(X):
    if X.shape[0] < 2:
        return [1] * X.shape[0]
    model = IsolationForest(contamination=0.1, random_state=42)
    return model.fit_predict(X)

def compute_severity_score(df):
    scores = []
    for _, row in df.iterrows():
        s = 0
        if row['level'] == 'ERROR':
            s += 5
        elif row['level'] == 'WARNING':
            s += 2
        if row['anomaly'] == -1:
            s += 3
        if any(k in row['message'].lower() for k in ['fail', 'panic', 'fatal']):
            s += 2
        scores.append(min(s, 10))
    return scores

def save_analysis_to_csv(df, filename, output_dir='analysis_reports'):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{filename}_analysis.csv")
    df.to_csv(path, index=False)
    return path

def save_summary_report(df, filename, output_dir='analysis_reports'):
    os.makedirs(output_dir, exist_ok=True)
    summary = df.describe(include='all')
    path = os.path.join(output_dir, f"{filename}_summary.csv")
    summary.to_csv(path)
    return path
