import torch
from torchvision import transforms, models
from PIL import Image

# Load model
model = models.regnet_y_400mf(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, 20)

model.load_state_dict(torch.load("model/best_model.pth", map_location="cpu"))
model.eval()

classes = [
    'Aloo_matar','Besan_cheela','Biryani','Chapathi','Chole_bature',
    'Dahl','Dhokla','Dosa','Gulab_jamun','Idli','Jalebi',
    'Kadai_paneer','Naan','Paani_puri','Pakoda','Pav_bhaji',
    'Poha','Rolls','Samosa','Vada_pav'
]

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

def predict(image):
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)
        probs = torch.nn.functional.softmax(outputs[0], dim=0)

    conf, pred = torch.max(probs, 0)

    return classes[pred], round(conf.item()*100,2)
