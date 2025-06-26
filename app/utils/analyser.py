import re
import csv
import os

def analyze_log_file(filepath):
    """
    Parses a log file to extract ERRORs and WARNINGs.
    Returns a list of dicts with: timestamp, level, message.
    """
    log_pattern = re.compile(r"\[(.*?)\]\s+(ERROR|WARNING)\s+(.*)")
    extracted = []

    with open(filepath, 'r') as f:
        for line in f:
            match = log_pattern.match(line.strip())
            if match:
                timestamp, level, message = match.groups()
                extracted.append({
                    'timestamp': timestamp,
                    'level': level,
                    'message': message
                })
    return extracted

def save_analysis_to_csv(log_filename, issues, output_dir='analysis_reports'):
    """
    Save the extracted issues to a CSV file.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join("analysis_reports", log_filename + "_analysis.csv")

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['timestamp', 'level', 'message'])
        writer.writeheader()
        writer.writerows(issues)

    return output_file

