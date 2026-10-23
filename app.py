import streamlit as st
from PIL import Image
from utils.predict import predict
from utils.multi_detect import split_and_predict  # NEW
from utils.nutrition import get_nutrition
from utils.advice import get_person_advice, get_food_info
from utils.data_analysis import plot_class_distribution
from utils.nutrition_tracker import calculate_nutrition
import plotly.express as px
import pandas as pd

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(page_title="Food Analyzer", layout="wide")
st.title("🍽️ AI Food Recognition & Nutrition App")

# =============================
# MENU
# =============================
menu = st.sidebar.selectbox(
    "Menu",
    ["Home", "Weekly Tracker", "Model Performance"]
)

# =============================
# HOME (MULTI-FOOD DETECTION)
# =============================
if menu == "Home":

    st.subheader("📸 Upload Food Image")

    person_label = st.selectbox(
        "Select Person Type",
        ["Normal Person", "Diabetes Patient", "BP Patient",
         "Heart Patient", "Pregnancy", "Baby", "Dialysis"]
    )

    mapping = {
        "Normal Person": "normal",
        "Diabetes Patient": "diabetes",
        "BP Patient": "bp",
        "Heart Patient": "heart",
        "Pregnancy": "pregnancy",
        "Baby": "baby",
        "Dialysis": "dialysis"
    }

    person_type = mapping[person_label]

    uploaded = st.file_uploader("Upload Image")

    if uploaded:

        image = Image.open(uploaded)

        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(image, use_container_width=True)

        with col2:

            # =============================
            # MULTI-FOOD DETECTION
            # =============================
            foods_detected = split_and_predict(image)

            st.subheader("🍽️ Detected Foods")

            total_cal = 0
            total_pro = 0
            total_fat = 0

            for food in foods_detected:

                st.success(food)

                nutrition = get_nutrition(food)

                total_cal += nutrition["calories"]
                total_pro += nutrition["protein"]
                total_fat += nutrition["fat"]

                st.write(f"Calories: {nutrition['calories']}")
                st.write(f"Protein: {nutrition['protein']}")
                st.write(f"Fat: {nutrition['fat']}")
                st.write("---")

            # =============================
            # TOTAL NUTRITION
            # =============================
            st.subheader("🔥 Total Nutrition")

            c1, c2, c3 = st.columns(3)
            c1.metric("Calories", total_cal)
            c2.metric("Protein", total_pro)
            c3.metric("Fat", total_fat)

            # PIE CHART
            fig = px.pie(
                names=["Protein", "Fat"],
                values=[total_pro, total_fat]
            )
            st.plotly_chart(fig, use_container_width=True)

            # =============================
            # INGREDIENTS
            # =============================
            st.subheader("🥗 Ingredients")

            for food in foods_detected:
                st.write(f"**{food}**: {get_food_info(food)['ingredients']}")

            # =============================
            # ADVICE
            # =============================
            st.subheader(f"💡 Advice for {person_label}")

            for food in foods_detected:
                advice = get_person_advice(food, person_type)
                st.write(f"**{food}**: {advice}")


# =============================
# WEEKLY TRACKER
# =============================
elif menu == "Weekly Tracker":

    st.title("📅 Weekly Food Tracker")

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    foods = [
        'Aloo_matar','Besan_cheela','Biryani','Chapathi','Chole_bature',
        'Dahl','Dhokla','Dosa','Gulab_jamun','Idli','Jalebi',
        'Kadai_paneer','Naan','Paani_puri','Pakoda','Pav_bhaji',
        'Poha','Rolls','Samosa','Vada_pav'
    ]

    if "weekly_data" not in st.session_state:
        st.session_state.weekly_data = {}

    day = st.selectbox("Select Day", days)
    food = st.selectbox("Select Food", foods)

    if food in ['Biryani','Pav_bhaji','Poha','Kadai_paneer']:
        quantity = st.number_input("Enter grams", 20, 500, 100)
    elif food in ['Idli','Chapathi','Naan','Samosa','Vada_pav']:
        quantity = st.number_input("Number of pieces", 1, 10, 1)
    else:
        quantity = st.number_input("Servings", 1, 5, 1)

    if st.button("Add / Update Day"):

        nutrition = get_nutrition(food)
        calc = calculate_nutrition(food, nutrition, quantity)

        st.session_state.weekly_data[day] = {
            "food": food,
            "quantity": quantity,
            "calories": calc["calories"],
            "protein": calc["protein"],
            "fat": calc["fat"]
        }

        st.success(f"{day} updated ✅")

    if len(st.session_state.weekly_data) > 0:

        data = []
        for d in days:
            if d in st.session_state.weekly_data:
                row = st.session_state.weekly_data[d]
                data.append({
                    "day": d,
                    "food": row["food"],
                    "quantity": row["quantity"],
                    "calories": row["calories"],
                    "protein": row["protein"],
                    "fat": row["fat"]
                })

        df = pd.DataFrame(data)

        st.plotly_chart(px.bar(df, x="day", y="calories"), use_container_width=True)
        st.plotly_chart(px.line(df, x="day", y="protein", markers=True), use_container_width=True)
        st.plotly_chart(px.line(df, x="day", y="fat", markers=True), use_container_width=True)

        st.dataframe(df)

        if st.button("Clear Weekly Data"):
            st.session_state.weekly_data = {}
            st.success("Data Cleared")


# =============================
# MODEL PERFORMANCE
# =============================
elif menu == "Model Performance":

    import json
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

    st.title("📊 Model Performance")

    metrics = json.load(open("model/metrics.json"))
    cm = np.load("model/confusion.npy")
    fpr, tpr = np.load("model/roc.npy", allow_pickle=True)
    loss = np.load("model/loss.npy")
    acc = np.load("model/acc.npy")

    st.subheader("📌 Metrics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", round(metrics['accuracy']*100, 2))
    col2.metric("Precision", round(metrics['weighted avg']['precision'], 2))
    col3.metric("Recall", round(metrics['weighted avg']['recall'], 2))
    col4.metric("F1 Score", round(metrics['weighted avg']['f1-score'], 2))

    st.subheader("🔲 Confusion Matrix")
    st.plotly_chart(px.imshow(cm, text_auto=True), use_container_width=True)

    st.subheader("📈 ROC Curve")
    st.plotly_chart(px.line(x=fpr, y=tpr), use_container_width=True)

    st.subheader("📉 Loss Curve")
    st.plotly_chart(px.line(y=loss), use_container_width=True)

    st.subheader("📈 Accuracy Curve")
    st.plotly_chart(px.line(y=acc), use_container_width=True)

    st.subheader("📊 Dataset Distribution")
    fig = plot_class_distribution("dataset")
    st.pyplot(fig)

    st.subheader("🔥 Nutrient Heatmap")
    df = pd.read_csv("data/nutrition.csv")
    plt.figure(figsize=(10,6))
    sns.heatmap(df.set_index("food"), cmap="coolwarm", annot=True)
    st.pyplot(plt)

    try:
        st.subheader("📈 Top-1 & Top-5 Accuracy")
        top1 = np.load("model/top1.npy")
        top5 = np.load("model/top5.npy")

        st.plotly_chart(px.line(y=top1, title="Top-1 Accuracy"))
        st.plotly_chart(px.line(y=top5, title="Top-5 Accuracy"))

    except:
        st.warning("Top-1 / Top-5 data not available.")
