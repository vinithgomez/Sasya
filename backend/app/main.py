import io
import json
from contextlib import asynccontextmanager
from pathlib import Path

import torch
import torch.nn.functional as F
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from torchvision import transforms
from torchvision.models import efficientnet_b0

MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "model" / "krishivision_model.pt"
TREATMENT_DATA_PATH = Path(__file__).resolve().parent / "treatment_data.json"

IMAGE_SIZE = 224
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# Same preprocessing as train.py's val_transform -- resize + normalize, no augmentation.
inference_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
])

model_state = {}


def load_model():
    checkpoint = torch.load(MODEL_PATH, map_location="cpu")
    class_names = checkpoint["class_names"]

    model = efficientnet_b0(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier[1] = torch.nn.Linear(in_features, len(class_names))
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    model_state["model"] = model
    model_state["class_names"] = class_names


def load_treatment_data():
    with open(TREATMENT_DATA_PATH, encoding="utf-8") as f:
        model_state["treatment_data"] = json.load(f)


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    load_treatment_data()
    yield


app = FastAPI(title="Plant Disease Detection API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")

    image_bytes = await file.read()
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="Could not read image file")

    input_tensor = inference_transform(image).unsqueeze(0)

    model = model_state["model"]
    class_names = model_state["class_names"]
    treatment_data = model_state["treatment_data"]

    with torch.no_grad():
        logits = model(input_tensor)
        probabilities = F.softmax(logits, dim=1)[0]
        confidence, predicted_idx = torch.max(probabilities, dim=0)

    predicted_class = class_names[predicted_idx.item()]
    treatment = treatment_data.get(predicted_class)

    return {
        "class": predicted_class,
        "confidence": float(confidence.item()),
        "is_healthy": treatment["is_healthy"] if treatment else None,
        "treatment": treatment,
    }
