# from PIL import Image, ImageDraw
# import os

# def annotate_image(image_path, output_dir="static/processed_images"):
#     os.makedirs(output_dir, exist_ok=True)

#     try:
#         with Image.open(image_path) as img:
#             if img.mode != "RGB":
#                 img = img.convert("RGB")

#             draw = ImageDraw.Draw(img)
#             draw.rectangle([50, 50, 200, 200], outline="red", width=4)
#             draw.text((60, 60), "Possible Defect", fill="red")

#             filename = os.path.basename(image_path)
#             base, ext = os.path.splitext(filename)
#             output_filename = f"annotated_{base}.jpg"

#             output_path = os.path.abspath(os.path.join(output_dir, output_filename))
#             img.save(output_path, format="JPEG")

#             print(f"[DEBUG] Save path: {output_path}")
#             print(f"[DEBUG] Exists? {os.path.exists(output_path)}")
#             print(f"[DEBUG] Annotated image save path: {os.path.abspath(output_path)}")
#             return output_filename 

#     except Exception as e:
#         print(f"❌ Error during annotation: {e}")
#         return None

#----------------------------------------------------------------------------
# --------------------------------------Currently working code.------------------------------
import cv2
from PIL import Image
import os

def annotate_faces_opencv(image_path, output_dir="static/processed_images"):
    os.makedirs(output_dir, exist_ok=True)

    # Load image using OpenCV
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load OpenCV's pre-trained face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    filename = os.path.basename(image_path)
    base, _ = os.path.splitext(filename)
    output_filename = f"face_annotated_{base}.jpg"
    output_path = os.path.join(output_dir, output_filename)
    cv2.imwrite(output_path, image)

    return output_filename

#----------------------------------------------------------------------------------------------------------

# import os
# import cv2
# from yolov8face import get_bbox
# import datetime

# def annotate_image(image_path, output_dir="static/processed_images"):
#     os.makedirs(output_dir, exist_ok=True)

#     img = cv2.imread(image_path)
#     if img is None:
#         print("❌ Could not read image")
#         return None

#     filename = os.path.basename(image_path)
#     timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
#     output_filename = f"annotated_{timestamp}_{filename}"
#     output_path = os.path.join(output_dir, output_filename)

#     # Get bounding boxes
#     bboxes = get_bbox(image_path)

#     if not bboxes:
#         print("⚠️ No faces detected, saving original image.")
#         cv2.imwrite(output_path, img)
#         return output_filename

#     for x1, y1, x2, y2, score in bboxes:
#         cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.putText(img, f"{score:.2f}", (x1, y1 - 5),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

#     cv2.imwrite(output_path, img)
#     return output_filename  
#----------------------------------------------------------------------------------------------------------


# import os
# import cv2
# import csv
# import datetime
# import numpy as np
# from PIL import Image, ExifTags
# from ultralytics import YOLO
# import imagehash

# # Load YOLOv8 Face Detection Model
# model = YOLO("yolov8n-face.pt")  # Place this in project root or adjust path

# # Output folders
# ANNOTATED_DIR = "static/processed_images"
# CSV_SUMMARY = "logs/face_summary.csv"

# os.makedirs(ANNOTATED_DIR, exist_ok=True)
# os.makedirs("logs", exist_ok=True)


# def fix_orientation(image_path):
#     try:
#         with Image.open(image_path) as img:
#             for orientation in ExifTags.TAGS:
#                 if ExifTags.TAGS[orientation] == 'Orientation':
#                     break
#             exif = img._getexif()
#             if exif is not None:
#                 orientation_value = exif.get(orientation)
#                 if orientation_value == 3:
#                     img = img.rotate(180, expand=True)
#                 elif orientation_value == 6:
#                     img = img.rotate(270, expand=True)
#                 elif orientation_value == 8:
#                     img = img.rotate(90, expand=True)
#             return img.convert("RGB")
#     except Exception as e:
#         print(f"⚠️ Orientation fix failed: {e}")
#         return Image.open(image_path).convert("RGB")


# def calculate_hash(image_path):
#     return str(imagehash.average_hash(Image.open(image_path)))


# def compare_images(img1_path, img2_path):
#     """Return SSIM similarity between two images."""
#     from skimage.metrics import structural_similarity as ssim
#     img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
#     img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
#     img1 = cv2.resize(img1, (300, 300))
#     img2 = cv2.resize(img2, (300, 300))
#     score, _ = ssim(img1, img2, full=True)
#     return score


# def annotate_image(image_path, output_dir=ANNOTATED_DIR, lang='en', mode='face'):
#     filename = os.path.basename(image_path)
#     base, _ = os.path.splitext(filename)
#     output_filename = f"annotated_{base}.jpg"
#     output_path = os.path.join(output_dir, output_filename)

#     try:
#         # Correct orientation
#         pil_image = fix_orientation(image_path)
#         image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

#         # Run YOLOv8 detection
#         results = model(image)[0]
#         bboxes = results.boxes.data.cpu().numpy() if results.boxes is not None else []

#         # Annotate detections
#         for i, (x1, y1, x2, y2, conf, cls) in enumerate(bboxes):
#             label = f"Face {i+1} ({conf:.2f})" if lang == 'en' else f"चेहरा {i+1} ({conf:.2f})"
#             x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
#             cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
#                         0.6, (0, 255, 0), 2)

#         # Add face count annotation
#         face_count = len(bboxes)
#         count_label = f"Faces detected: {face_count}" if lang == 'en' else f"चेहरे मिले: {face_count}"
#         cv2.putText(image, count_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
#                     1, (255, 255, 255), 2)

#         # Save annotated image
#         cv2.imwrite(output_path, image)

#         # Save CSV summary
#         with open(CSV_SUMMARY, 'a', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow([
#                 base, face_count,
#                 datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                 calculate_hash(image_path)
#             ])

#         return f"processed_images/{output_filename}"

#     except Exception as e:
#         print(f"❌ Error in annotate_image: {e}")
#         return None
