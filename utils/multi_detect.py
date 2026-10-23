from PIL import Image
from utils.predict import predict

def split_and_predict(image):

    width, height = image.size

    # Split into 4 parts
    crops = [
        image.crop((0, 0, width//2, height//2)),
        image.crop((width//2, 0, width, height//2)),
        image.crop((0, height//2, width//2, height)),
        image.crop((width//2, height//2, width, height))
    ]

    results = []

    for crop in crops:
        food, conf = predict(crop)

        # Avoid duplicates
        if food not in results and conf > 50:
            results.append(food)

    return results
