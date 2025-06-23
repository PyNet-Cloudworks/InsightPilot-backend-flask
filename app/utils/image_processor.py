from PIL import Image, ImageDraw
import os

def annotate_image(image_path, output_dir="static/processed_images"):
    os.makedirs(output_dir, exist_ok=True)

    try:
        with Image.open(image_path) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")

            draw = ImageDraw.Draw(img)
            draw.rectangle([50, 50, 200, 200], outline="red", width=4)
            draw.text((60, 60), "Possible Defect", fill="red")

            filename = os.path.basename(image_path)
            base, ext = os.path.splitext(filename)
            output_filename = f"annotated_{base}.jpg"

            output_path = os.path.abspath(os.path.join(output_dir, output_filename))
            img.save(output_path, format="JPEG")

            print(f"[DEBUG] Save path: {output_path}")
            print(f"[DEBUG] Exists? {os.path.exists(output_path)}")
            print(f"[DEBUG] Annotated image save path: {os.path.abspath(output_path)}")
            return output_filename 

    except Exception as e:
        print(f"❌ Error during annotation: {e}")
        return None
