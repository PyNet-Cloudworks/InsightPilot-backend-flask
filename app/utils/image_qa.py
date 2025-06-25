import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def is_blurry(image_cv, threshold=100):
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return lap_var < threshold, lap_var

def is_too_dark_or_bright(image_cv, dark_thresh=50, bright_thresh=200):
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    avg_intensity = np.mean(gray)
    if avg_intensity < dark_thresh:
        return "Too Dark", avg_intensity
    elif avg_intensity > bright_thresh:
        return "Too Bright", avg_intensity
    return "Normal", avg_intensity

def analyze_image(image_path):
    image_cv = cv2.imread(image_path)
    results = []

    blurry, score = is_blurry(image_cv)
    if blurry:
        results.append({'issue': 'Blurry Image', 'score': round(score, 2)})

    lighting_status, avg_light = is_too_dark_or_bright(image_cv)
    if lighting_status != "Normal":
        results.append({'issue': lighting_status, 'score': round(avg_light, 2)})

    return results
