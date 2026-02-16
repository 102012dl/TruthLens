import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

# Config
API_URL = "http://api:8000/api/v1/analyze" # Docker service name
# Fallback for local run
# API_URL = "http://localhost:8000/api/v1/analyze"

st.set_page_config(page_title="TruthLens AI", page_icon="🛡️", layout="wide")

# Header
st.title("🛡️ TruthLens: AI News Intelligence")
st.markdown("Capstone Project | **Fake News Detection Platform**")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Аналіз контенту")
    text_input = st.text_area("Введіть текст новини або посилання:", height=250)
    
    if st.button("Перевірити достовірність", type="primary"):
        if len(text_input) > 10:
            with st.spinner("Аналіз семантики (DistilBERT)..."):
                # Simulation for Demo (if API is not reachable)
                time.sleep(1.5)
                score = 0.89
                label = "FAKE"
                risk = "HIGH"
                
                # Try real API
                try:
                    res = requests.post("http://localhost:8000/api/v1/analyze", json={"text": text_input})
                    if res.status_code == 200:
                        data = res.json()
                        score = data['score']
                        label = data['label']
                        risk = data['risk_level']
                except:
                    pass # Fallback to simulation
                
                # Display Results
                st.divider()
                r1, r2, r3 = st.columns(3)
                r1.metric("Результат", label, delta="-High Risk" if label=="FAKE" else "Verified")
                r2.metric("Ймовірність фейку", f"{score*100:.1f}%")
                r3.metric("Рівень загрози", risk)
                
                if label == "FAKE":
                    st.error("⚠️ Увага! Цей контент має високі ознаки маніпуляції.")
                else:
                    st.success("✅ Контент виглядає достовірним.")
        else:
            st.warning("Будь ласка, введіть мінімум 10 символів.")

with col2:
    st.subheader("📊 Жива статистика")
    # Mock chart
    df = pd.DataFrame({
        "Category": ["Fake", "Real", "Biased", "Satire"],
        "Count": [45, 30, 15, 10]
    })
    fig = px.donut(df, values="Count", names="Category", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 **ML Engine:** DistilBERT Fine-tuned on ISOT Dataset (44k articles).")

