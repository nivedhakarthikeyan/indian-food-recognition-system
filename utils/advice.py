def get_food_info(food):

    data = {
        "Biryani": {"ingredients": "Rice, Chicken, Oil, Spices"},
        "Idli": {"ingredients": "Rice, Urad dal"},
        "Chapathi": {"ingredients": "Wheat flour"},
        "Dosa": {"ingredients": "Rice, Oil"},
        "Gulab_jamun": {"ingredients": "Sugar, Milk solids, Oil"},
        "Poha": {"ingredients": "Flattened rice, Vegetables"},
        "Samosa": {"ingredients": "Potato, Oil, Flour"}
    }

    return data.get(food, {"ingredients": "Common Indian ingredients"})


def get_person_advice(food, person_type):

    advice = {

        "diabetes": {
            "Biryani": "❌ High carbs — avoid or take small portion.",
            "Gulab_jamun": "❌ High sugar — strictly avoid.",
            "Chapathi": "✅ Better than rice, consume in moderation.",
            "Poha": "⚠ Moderate carbs — take limited quantity.",
            "Idli": "⚠ Slightly high carbs — eat in small quantity."
        },

        "bp": {
            "Biryani": "❌ High salt & oil — avoid.",
            "Chapathi": "✅ Low salt — good choice.",
            "Poha": "✅ Light and safe food.",
            "Samosa": "❌ Fried food — avoid."
        },

        "heart": {
            "Biryani": "❌ High fat — avoid.",
            "Gulab_jamun": "❌ High sugar & oil — avoid.",
            "Chapathi": "✅ Low fat — good.",
            "Poha": "✅ Light and heart-friendly.",
            "Pakoda": "❌ Fried food — avoid."
        },

        "pregnancy": {
            "Biryani": "⚠ Eat occasionally, avoid excess spices.",
            "Idli": "✅ Safe and easy to digest.",
            "Poha": "✅ Good for digestion."
        },

        "baby": {
            "Idli": "✅ Soft and easy to digest.",
            "Chapathi": "⚠ Give in mashed form.",
            "Biryani": "❌ Too spicy for babies.",
            "Poha": "✅ Soft and suitable."
        },

        "dialysis": {
            "Biryani": "❌ High sodium — avoid.",
            "Chapathi": "⚠ Limit intake.",
            "Poha": "⚠ Moderate consumption."
        },

        "normal": {
            "Biryani": "⚠ Eat occasionally.",
            "Chapathi": "✅ Healthy option.",
            "Poha": "✅ Light and healthy.",
            "Gulab_jamun": "⚠ Limit sweets."
        }
    }

    person_data = advice.get(person_type, {})

    # 🔥 IMPORTANT FIX: EXACT MATCH
    if food in person_data:
        return person_data[food]
    else:
        return "⚠ Eat in moderation and maintain a balanced diet."
