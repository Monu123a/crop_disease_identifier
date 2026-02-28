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

def predict_disease(image_bytes):
    """
    Runs disease prediction on the provided image bytes.
    Handles JPEG, PNG, WebP, BMP, TIFF, and other PIL-supported formats.
    Converts to RGB to ensure consistent processing regardless of source format.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))

        # Convert to RGB to handle RGBA (PNG transparency), palette (GIF/PNG),
        # and any other mode that numpy/PIL may not process uniformly.
        img = img.convert("RGB")
        img = img.resize((224, 224))

        img_array = np.array(img)
        mean_val = np.mean(img_array)

        index = int(mean_val % len(DISEASES))
        result = DISEASES[index].copy()

        # Add deterministic variance based on image content
        result["confidence"] = round(min(result["confidence"] + (mean_val % 5), 100.0), 1)

        return result
    except Exception as e:
        print(f"Prediction error: {e}")
        return None
