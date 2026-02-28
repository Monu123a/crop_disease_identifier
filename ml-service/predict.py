import numpy as np
from PIL import Image
import io
import json
import os
import tensorflow as tf

# ── Paths ──────────────────────────────────────────────────────────────────
_DIR = os.path.dirname(__file__)
MODEL_PATH       = os.path.join(_DIR, 'plant_disease_model.keras')
CLASS_NAMES_PATH = os.path.join(_DIR, 'class_names.json')

# ── Load model & class names once at startup ───────────────────────────────
print("[INFO] Loading model…")
model = tf.keras.models.load_model(MODEL_PATH)
print(f"[INFO] Model loaded. Input: {model.input_shape}  Output: {model.output_shape}")

with open(CLASS_NAMES_PATH) as f:
    CLASS_NAMES = json.load(f)

print(f"[INFO] Classes ({len(CLASS_NAMES)}): {CLASS_NAMES}")

# ── Disease metadata keyed by class name ───────────────────────────────────
# Add/edit entries to match your class_names.json labels.
DISEASE_INFO = {
    "Pepper__bell___Bacterial_spot": {
        "disease":      "Pepper Bell – Bacterial Spot",
        "severity":     "Medium",
        "treatment":    "Apply copper-based bactericide. Remove and destroy infected leaves immediately.",
        "affectedCrops":"Bell Peppers, Chilli Peppers",
        "prevention":   "Use disease-free seeds, avoid overhead irrigation, and practice crop rotation.",
        "nextSteps":    ["Remove infected plant parts", "Apply copper spray", "Improve air circulation"],
    },
    "Pepper__bell___healthy": {
        "disease":      "Healthy Pepper Plant",
        "severity":     "None",
        "treatment":    "No treatment required. Plant appears healthy.",
        "affectedCrops":"All pepper varieties",
        "prevention":   "Continue regular monitoring, proper watering, and fertilisation.",
        "nextSteps":    ["Maintain regular irrigation", "Monitor weekly for early signs"],
    },
    "Potato___Early_blight": {
        "disease":      "Potato – Early Blight",
        "severity":     "Medium",
        "treatment":    "Apply chlorothalonil or mancozeb fungicide. Remove affected lower leaves.",
        "affectedCrops":"Potatoes, Tomatoes",
        "prevention":   "Use certified disease-free seed potatoes and avoid wetting foliage.",
        "nextSteps":    ["Remove infected leaves", "Apply fungicide spray", "Avoid overhead watering"],
    },
    "Potato___Late_blight": {
        "disease":      "Potato – Late Blight",
        "severity":     "High",
        "treatment":    "Apply metalaxyl or cymoxanil fungicide immediately. Destroy infected plants.",
        "affectedCrops":"Potatoes, Tomatoes, Peppers",
        "prevention":   "Use resistant varieties and ensure good drainage.",
        "nextSteps":    ["Isolate infected area", "Apply systemic fungicide", "Destroy severely infected plants"],
    },
    "Potato___healthy": {
        "disease":      "Healthy Potato Plant",
        "severity":     "None",
        "treatment":    "No treatment required. Plant appears healthy.",
        "affectedCrops":"All potato varieties",
        "prevention":   "Continue standard care. Scout weekly for blight symptoms.",
        "nextSteps":    ["Maintain hilling", "Monitor for late blight signs after rain"],
    },
    "Tomato___Bacterial_spot": {
        "disease":      "Tomato – Bacterial Spot",
        "severity":     "Medium",
        "treatment":    "Apply copper-based bactericide. Remove infected leaves and avoid wetting foliage.",
        "affectedCrops":"Tomatoes, Peppers",
        "prevention":   "Use resistant varieties, sanitise tools, and use drip irrigation.",
        "nextSteps":    ["Remove infected leaves", "Apply copper bactericide", "Use drip irrigation"],
    },
    "Tomato___Early_blight": {
        "disease":      "Tomato – Early Blight",
        "severity":     "Medium",
        "treatment":    "Apply mancozeb or chlorothalonil. Mulch around base to reduce soil splash.",
        "affectedCrops":"Tomatoes, Potatoes",
        "prevention":   "Remove lower leaves, water at base, and rotate crops annually.",
        "nextSteps":    ["Remove lower infected leaves", "Apply fungicide", "Mulch soil surface"],
    },
    "Tomato___Late_blight": {
        "disease":      "Tomato – Late Blight",
        "severity":     "High",
        "treatment":    "Apply metalaxyl fungicide immediately. Remove and destroy infected plants.",
        "affectedCrops":"Tomatoes, Potatoes",
        "prevention":   "Use resistant varieties, ensure air circulation, avoid wet foliage at night.",
        "nextSteps":    ["Isolate crop area", "Apply systemic fungicide", "Monitor neighbours"],
    },
    "Tomato___Leaf_Mold": {
        "disease":      "Tomato – Leaf Mold",
        "severity":     "Medium",
        "treatment":    "Apply chlorothalonil or copper fungicide. Improve ventilation in greenhouse.",
        "affectedCrops":"Tomatoes",
        "prevention":   "Reduce humidity, improve airflow, and avoid overhead watering.",
        "nextSteps":    ["Improve ventilation", "Remove infected leaves", "Apply fungicide"],
    },
    "Tomato___Septoria_leaf_spot": {
        "disease":      "Tomato – Septoria Leaf Spot",
        "severity":     "Medium",
        "treatment":    "Apply copper or mancozeb fungicide. Remove affected leaves from base up.",
        "affectedCrops":"Tomatoes",
        "prevention":   "Mulch soil, use drip irrigation, and remove lower leaves before symptoms worsen.",
        "nextSteps":    ["Remove lowest infected leaves", "Apply fungicide", "Avoid wetting foliage"],
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "disease":      "Tomato – Spider Mites",
        "severity":     "Medium",
        "treatment":    "Apply insecticidal soap or neem oil. Introduce predatory mites as biocontrol.",
        "affectedCrops":"Tomatoes, Beans, Cucumbers",
        "prevention":   "Maintain adequate moisture, avoid plant stress, and remove weeds nearby.",
        "nextSteps":    ["Apply neem oil spray", "Increase irrigation", "Inspect undersides of leaves"],
    },
    "Tomato___Target_Spot": {
        "disease":      "Tomato – Target Spot",
        "severity":     "Medium",
        "treatment":    "Apply chlorothalonil or azoxystrobin fungicide. Remove infected leaves.",
        "affectedCrops":"Tomatoes",
        "prevention":   "Avoid dense planting, maintain airflow, and use mulch.",
        "nextSteps":    ["Remove infected foliage", "Apply fungicide", "Improve plant spacing"],
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "disease":      "Tomato – Yellow Leaf Curl Virus",
        "severity":     "High",
        "treatment":    "No cure. Remove and destroy infected plants to prevent spread via whiteflies.",
        "affectedCrops":"Tomatoes",
        "prevention":   "Use resistant varieties, control whitefly populations, and use reflective mulch.",
        "nextSteps":    ["Remove infected plants", "Control whitefly with insecticide", "Use resistant varieties next season"],
    },
    "Tomato___Tomato_mosaic_virus": {
        "disease":      "Tomato – Mosaic Virus",
        "severity":     "High",
        "treatment":    "No cure. Remove infected plants, sanitise hands and tools between plants.",
        "affectedCrops":"Tomatoes, Peppers, Cucumbers",
        "prevention":   "Use virus-free transplants, control aphids, and avoid tobacco near plants.",
        "nextSteps":    ["Destroy infected plants", "Disinfect tools with bleach solution", "Control aphid vectors"],
    },
    "Tomato___healthy": {
        "disease":      "Healthy Tomato Plant",
        "severity":     "None",
        "treatment":    "No treatment required. Plant appears healthy.",
        "affectedCrops":"All tomato varieties",
        "prevention":   "Continue standard care, monitor weekly, and maintain soil health.",
        "nextSteps":    ["Maintain regular irrigation", "Inspect weekly for early symptoms"],
    },
}

# Fallback for any class not in DISEASE_INFO
_DEFAULT_INFO = {
    "severity":     "Unknown",
    "treatment":    "Consult a local agronomist for diagnosis and treatment recommendations.",
    "affectedCrops":"Various crops",
    "prevention":   "Monitor regularly and maintain good agricultural practices.",
    "nextSteps":    ["Consult an agronomist", "Isolate affected area", "Monitor neighbouring plants"],
}


def _preprocess(image_bytes):
    """Open image bytes, resize to 224×224, normalise to [0, 1]."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)          # (1, 224, 224, 3)


def predict_disease(image_bytes):
    """
    Run real Keras model inference on an image.
    Returns a result dict compatible with the frontend ResultCard,
    or None on error.
    """
    try:
        img_tensor = _preprocess(image_bytes)

        preds       = model.predict(img_tensor, verbose=0)[0]   # shape (15,)
        idx         = int(np.argmax(preds))
        confidence  = float(preds[idx])
        class_name  = CLASS_NAMES[idx]

        print(f"[INFO] Predicted: {class_name} ({confidence*100:.1f}%)")

        info = DISEASE_INFO.get(class_name, {**_DEFAULT_INFO, "disease": class_name.replace("_", " ")}).copy()
        info["confidence"] = round(min(confidence * 100, 100.0), 1)
        return info

    except Exception as e:
        print(f"Prediction error: {e}")
        return None
