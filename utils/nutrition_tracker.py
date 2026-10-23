def calculate_nutrition(food, nutrition_data, quantity):

    gram_foods = ['Biryani', 'Pav_bhaji', 'Poha', 'Kadai_paneer']
    piece_foods = ['Idli', 'Chapathi', 'Naan', 'Samosa', 'Vada_pav']

    if food in gram_foods:
        factor = quantity / 100

    elif food in piece_foods:
        factor = quantity

    else:
        factor = quantity

    return {
        "calories": int(nutrition_data["calories"] * factor),
        "protein": int(nutrition_data["protein"] * factor),
        "fat": int(nutrition_data["fat"] * factor)
    }
