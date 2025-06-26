from datetime import datetime
import os
import cv2
from app.utils.image_processor import annotate_faces_opencv, detect_defects_opencv

def extract_keyframes(video_path, output_dir="static/video_frames"):
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(video_path)
    prefix = datetime.now().strftime('%Y%m%d_%H%M%S_') + base_name

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    results = {
        "face": [],
        "defect": [],
        "raw": []
    }

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % 90 == 0:
            raw_frame_name = f"{prefix}_frame_{frame_count}.jpg"
            raw_path = os.path.join(output_dir, raw_frame_name)
            cv2.imwrite(raw_path, frame)
            results["raw"].append(raw_frame_name)

            # Run face and defect detectors
            face_annotated = annotate_faces_opencv(raw_path)
            defect_annotated = detect_defects_opencv(raw_path)

            if face_annotated:
                results["face"].append(face_annotated)
            if defect_annotated:
                results["defect"].append(defect_annotated)

        frame_count += 1

    cap.release()
    return results  # ⬅ returns dict of lists: face, defect, raw
