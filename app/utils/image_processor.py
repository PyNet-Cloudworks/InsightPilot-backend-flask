import cv2
import os

# ------------------- FACE DETECTION -------------------

def annotate_faces_opencv(image_path, output_dir="static/processed_images", return_img=False):
    os.makedirs(output_dir, exist_ok=True)

    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Could not load image: {image_path}")
        return (0, None) if return_img else None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use OpenCV's face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 0), 2)

    filename = os.path.basename(image_path)
    base, _ = os.path.splitext(filename)
    output_filename = f"face_annotated_{base}.jpg"
    output_path = os.path.join(output_dir, output_filename)
    cv2.imwrite(output_path, image)

    if return_img:
        return len(faces), image
    return output_filename


# ------------------- DEFECT DETECTION -------------------

def detect_defects_opencv(image_path, output_dir="static/processed_images", return_img=False):
    os.makedirs(output_dir, exist_ok=True)

    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Could not read image: {image_path}")
            return (0, None) if return_img else None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        defect_count = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 200:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)

            # Labeling logic
            if area > 1000 and aspect_ratio < 1.5:
                label = "Dent"
            elif aspect_ratio > 3:
                label = "Scratch"
            elif area > 700 and aspect_ratio > 1.5:
                label = "Crack"
            else:
                label = "Defect"

            defect_count += 1
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        filename = os.path.basename(image_path)
        base, _ = os.path.splitext(filename)
        output_filename = f"defect_annotated_{base}.jpg"
        output_path = os.path.join(output_dir, output_filename)
        cv2.imwrite(output_path, image)

        if return_img:
            return defect_count, image
        return output_filename

    except Exception as e:
        print(f"❌ Error during defect detection: {e}")
        return (0, None) if return_img else None
