import numpy as np
from PIL import Image
import io

# Mock disease database
DISEASES = [
    {
        "disease": "Tomato Late Blight",
        "severity": "High",
        "confidence": 94,
        "treatment": "Apply fungicide containing chlorothalonil or copper. Remove and destroy infected plants.",
        "affectedCrops": "Tomatoes, Potatoes, Peppers",
        "prevention": "Use resistant varieties and improve air circulation.",
        "nextSteps": ["Isolate the crop area", "Clean all farming tools"]
    },
    {
        "disease": "Apple Scab",
        "severity": "Medium",
        "confidence": 88,
        "treatment": "Apply sulfur-based fungicides or neem oil. Rake and destroy fallen leaves.",
        "affectedCrops": "Apples, Pears",
        "prevention": "Prune trees to improve light penetration and air flow.",
        "nextSteps": ["Remove infected leaves", "Prune for airflow"]
    },
    {
        "disease": "Healthy Leaf",
        "severity": "Low",
        "confidence": 99,
        "treatment": "No treatment required. Plant is healthy.",
        "affectedCrops": "All crops",
        "prevention": "Continue standard care and monitoring.",
        "nextSteps": ["Maintain regular irrigation", "Inspect weekly"]
    }
]

# Minimum fraction of "vegetation-like" pixels required to accept an image.
# Real leaves (even diseased/yellow/brown ones) easily exceed 8%.
# Non-plant photos (faces, buildings, food, etc.) typically fall well below this.
VEGETATION_THRESHOLD = 0.08


def detect_vegetation_ratio(img_array):
    """
    Return the fraction of pixels that look like plant/vegetation.

    Strategy (all in plain numpy, no extra dependencies):
      - Pure green: G channel clearly dominates R and B (typical healthy leaf)
      - Yellow-green: G > B by a healthy margin and neither R nor G is near 0
        (covers yellowing, light-stressed, or diseased leaves)
      - Dark green: G beats both channels even at lower absolute values
        (covers shaded or very deep-green leaves)
    """
    r = img_array[:, :, 0].astype(np.float32)
    g = img_array[:, :, 1].astype(np.float32)
    b = img_array[:, :, 2].astype(np.float32)

    pure_green   = (g > r * 1.10) & (g > b * 1.10)
    yellow_green = (g > b * 1.15) & (r > 40) & (g > 60)
    dark_green   = (g > r) & (g > b) & (g > 40)

    vegetation_mask = pure_green | yellow_green | dark_green
    return float(vegetation_mask.sum()) / vegetation_mask.size


def predict_disease(image_bytes):
    """
    Runs disease prediction on the provided image bytes.
    Returns a result dict, a no-crop-detected dict, or None on error.

    Handles JPEG, PNG, WebP, BMP, TIFF, and other PIL-supported formats.
    Rejects images that do not contain enough green/vegetation pixels.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))

        # Normalise mode (handles RGBA, palette, etc.)
        img = img.convert("RGB")
        img = img.resize((224, 224))

        img_array = np.array(img)

        # ── Vegetation check ──────────────────────────────────────────────
        veg_ratio = detect_vegetation_ratio(img_array)
        print(f"[INFO] vegetation ratio = {veg_ratio:.3f}")

        if veg_ratio < VEGETATION_THRESHOLD:
            return {
                "noCropDetected": True,
                "message": (
                    "No crop or plant detected in this image. "
                    "Please upload a clear photo of a leaf or vegetable."
                )
            }
        # ─────────────────────────────────────────────────────────────────

        mean_val = np.mean(img_array)
        index    = int(mean_val % len(DISEASES))
        result   = DISEASES[index].copy()

        result["confidence"] = round(min(result["confidence"] + (mean_val % 5), 100.0), 1)

        return result

    except Exception as e:
        print(f"Prediction error: {e}")
        return None
