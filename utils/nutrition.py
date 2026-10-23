import pandas as pd

# Load CSV
df = pd.read_csv("data/nutrition.csv")

def get_nutrition(food_name):

    # Clean names (important fix)
    food_name = food_name.strip()

    row = df[df['food'] == food_name]

    if not row.empty:
        return {
            "calories": int(row.iloc[0]['calories']),
            "protein": int(row.iloc[0]['protein']),
            "fat": int(row.iloc[0]['fat']),
            "carbs": int(row.iloc[0]['carbs'])
        }
    else:
        # Debug print (optional)
        print("Food not found:", food_name)

        return {
            "calories": 0,
            "protein": 0,
            "fat": 0,
            "carbs": 0
        }
