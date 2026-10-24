
import os
import json
import torch
from torchvision import transforms, models
from PIL import Image

# =============================
# SETTINGS
# =============================
MODEL_PATH = "model/best_model.pth"
CLASS_MAPPING_PATH = "class_mapping.json"
NUM_CLASSES = 20

device = torch.device("cpu")

# =============================
# LOAD CLASS NAMES
# =============================
default_classes = [
    "Aloo_matar",
    "Besan_cheela",
    "Biryani",
    "Chapathi",
    "Chole_bature",
    "Dahl",
    "Dhokla",
    "Dosa",
    "Gulab_jamun",
    "Idli",
    "Jalebi",
    "Kadai_paneer",
    "Naan",
    "Paani_puri",
    "Pakoda",
    "Pav_bhaji",
    "Poha",
    "Rolls",
    "Samosa",
    "Vada_pav"
]

if os.path.exists(CLASS_MAPPING_PATH):
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        classes = json.load(f)
else:
    classes = default_classes

if len(classes) != NUM_CLASSES:
    raise ValueError(
        f"Expected {NUM_CLASSES} classes, but found {len(classes)}."
    )

# =============================
# LOAD MODEL
# =============================
model = models.regnet_y_400mf(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, NUM_CLASSES)

state_dict = torch.load(MODEL_PATH, map_location=device)
model.load_state_dict(state_dict)
model.to(device)
model.eval()

# =============================
# IMAGE TRANSFORM
# Keep this consistent with training
# =============================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# =============================
# PREDICTION
# =============================
def predict(image):
    if not isinstance(image, Image.Image):
        image = Image.open(image)

    image = image.convert("RGB")
    image_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs[0], dim=0)

    confidence, pred_index = torch.max(probabilities, dim=0)

    predicted_class = classes[pred_index.item()]
    confidence_percent = round(confidence.item() * 100, 2)

    return predicted_class, confidence_percent
