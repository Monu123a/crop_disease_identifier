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
    Simulates model inference. In a real scenario, this would:
    1. Load a .h5 or .keras model
    2. Preprocess the image
    3. Run model.predict()
    """
    try:
        # Simulate processing time
        img = Image.open(io.BytesIO(image_bytes))
        img = img.resize((224, 224))
        
        # Logic to "randomly" but consistently pick a result based on image mean
        # This makes it feel more "real" during testing
        img_array = np.array(img)
        mean_val = np.mean(img_array)
        
        index = int(mean_val % len(DISEASES))
        result = DISEASES[index].copy()
        
        # Add some randomness to confidence
        result["confidence"] = round(result["confidence"] + (mean_val % 5), 1)
        
        return result
    except Exception as e:
        print(f"Prediction error: {e}")
        return None
