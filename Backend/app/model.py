import os
import json
import numpy as np
import tensorflow as tf
# from tensorflow.keras.applications import MobileNetV2
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

from tensorflow.keras.preprocessing import image



# LOCAL_WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "models", "resnet50_weights.h5")

# resnet_model = ResNet50(weights=LOCAL_WEIGHTS_PATH)




# Path to local ImageNet index
IMAGENET_INDEX_PATH = os.path.join(
    os.path.dirname(__file__), "imagenet_class_index.json"
)

# Load ImageNet class index once
with open(IMAGENET_INDEX_PATH) as f:
    IMAGENET_CLASS_INDEX = json.load(f)

def custom_decode_predictions(preds, top=3):
    """Offline version of Keras decode_predictions."""
    results = []
    for pred in preds:
        top_indices = pred.argsort()[-top:][::-1]
        top_results = []
        for i in top_indices:
            class_id, class_name = IMAGENET_CLASS_INDEX[str(i)]
            top_results.append((class_id, class_name, float(pred[i])))
        results.append(top_results)
    return results

# Read weights path from environment (default: ImageNet)
# MODEL_WEIGHTS_PATH = os.getenv("MOBILENET_WEIGHTS_PATH", "imagenet")

# Load model once at startup
# mobilenet_model = MobileNetV2(weights=MODEL_WEIGHTS_PATH)

MODEL_WEIGHTS_PATH = os.getenv("RESNET_WEIGHTS_PATH", "imagenet")

resnet_model = ResNet50(weights=MODEL_WEIGHTS_PATH)




# Define your custom mappings
TYPE_CLASSES = ["Plastic", "Metal", "Paper"]
BRAND_CLASSES = ["Pepsi", "Dasani", "Other"]

def predict_image(path: str):
    """
    Run inference using MobileNetV2, then map predictions to Type/Brand.
    Returns a dict with type, brand, confidence, and reasoning.
    """

    try:
        # Load + preprocess image
        img = image.load_img(path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Predict
        preds = resnet_model.predict(x)
        decoded = decode_predictions(preds, top=3)[0]


        # Example: use the top-1 prediction
        _, label, prob = decoded[0]  # (class_id, class_name, confidence)

        # ---- Mapping logic ----
        label_lower = label.lower()

        # Type mapping
        if any(word in label_lower for word in ["bottle", "plastic"]):
            item_type = "Plastic"
        elif any(word in label_lower for word in ["can", "tin", "metal"]):
            item_type = "Metal"
        elif any(word in label_lower for word in ["paper", "carton"]):
            item_type = "Paper"
        else:
            item_type = np.random.choice(TYPE_CLASSES)

        # Brand mapping (dummy heuristic)
        if "pepsi" in label_lower:
            brand = "Pepsi"
        elif "dasani" in label_lower:
            brand = "Dasani"
        else:
            brand = "Other"

        confidence = float(prob)
        reasoning = f"MobileNet predicted '{label}' ({prob:.2f}) → mapped to {item_type}, {brand}"

        return {
            "type": item_type,
            "brand": brand,
            "confidence": confidence,
            "reasoning": reasoning,
        }

    except Exception as e:
        # Handle errors gracefully
        return {
            "type": "Unknown",
            "brand": "Unknown",
            "confidence": 0.0,
            "reasoning": f"Prediction failed: {str(e)}"
        }
