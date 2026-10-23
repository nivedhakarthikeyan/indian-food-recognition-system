from ultralytics import YOLO

# load trained model (you can use pretrained or your custom)
model = YOLO("yolov8n.pt")  # later replace with your trained food model

def detect_foods(image):
    results = model(image)

    detections = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]
            conf = float(box.conf[0])

            detections.append({
                "food": label,
                "confidence": round(conf * 100, 2)
            })

    return detections
