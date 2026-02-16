import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Config
API_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="TruthLens Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ TruthLens: AI News Intelligence")
st.markdown("### Automated Fake News Detection & Sentiment Analysis")

# Input Section
col1, col2 = st.columns([2, 1])

with col1:
    news_text = st.text_area("Вставте текст новини для аналізу:", height=200)
    if st.button("🔍 Аналізувати"):
        if news_text:
            try:
                # Mock request to FastAPI (replace with real request when Docker is up)
                # response = requests.post(API_URL, json={"text": news_text})
                # data = response.json()
                
                # Mock Data for Demo
                data = {"score": 0.88, "label": "FAKE", "risk_level": "HIGH"}
                
                st.success(f"Результат: {data['label']}")
                st.metric("Ймовірність фейку", f"{data['score']*100:.1f}%")
                
                if data['risk_level'] == "HIGH":
                    st.error("⚠️ Високий ризик дезінформації!")
            except Exception as e:
                st.error(f"Помилка з'єднання з API: {e}")
        else:
            st.warning("Будь ласка, введіть текст.")

with col2:
    st.info("ℹ️ Як це працює")
    st.write("TruthLens використовує модель DistilBERT, навчену на 44k+ статтях, для виявлення семантичних патернів дезінформації.")

# Visuals from your previous plan
st.divider()
st.subheader("📊 Статистика аналізу")
chart_data = pd.DataFrame({
    "Category": ["Fake", "Real", "Biased"],
    "Count": [450, 320, 150]
})
fig = px.pie(chart_data, values="Count", names="Category", title="Розподіл проаналізованих новин")
st.plotly_chart(fig)
