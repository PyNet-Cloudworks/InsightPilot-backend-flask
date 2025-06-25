import cv2
import os
from datetime import datetime

def detect_faces_dnn(image_path, output_dir="static/processed_images", model_dir="app/models"):
    os.makedirs(output_dir, exist_ok=True)

    # Load DNN model
    prototxt_path = os.path.join(model_dir, "deploy.prototxt")
    model_path = os.path.join(model_dir, "res10_300x300_ssd_iter_140000.caffemodel")

    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

    # Read image
    image = cv2.imread(image_path)
    # image = cv2.resize(image, (800, 800))  # Resize for consistent behavior
    if image is None:
        print(f"❌ Could not read image: {image_path}")
        return None

    (h, w) = image.shape[:2]
    if max(h, w) > 800:
        image = cv2.resize(image, (800, int(h * 800 / w)))
        
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))  # Mean subtraction for better accuracy

    net.setInput(blob)
    detections = net.forward()

    face_count = 0
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.3:  # Confidence threshold
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
            text = f"{int(confidence * 100)}%"
            cv2.putText(image, text, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
            face_count += 1

    # Annotate total faces detected
    cv2.putText(image, f"Faces: {face_count}", (10, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Save
    base = os.path.basename(image_path)
    name, _ = os.path.splitext(base)
    output_path = os.path.join(output_dir, f"annotated_{name}.jpg")
    cv2.imwrite(output_path, image)
    print(f"✅ Saved annotated image: {output_path}")

    return os.path.basename(output_path)  # return just the filename
