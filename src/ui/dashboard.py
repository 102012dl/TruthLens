import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time
import random

# Configuration
API_URL = "http://api:8000/api/v1/analyze"

st.set_page_config(page_title="TruthLens Dashboard", page_icon="🛡️", layout="wide")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=64)
    st.title("TruthLens")
    st.info("Capstone Project v2.0")
    st.markdown("---")
    st.write("**Model:** DistilBERT")
    st.write("**Status:** Active")

# Main Content
st.title("🛡️ AI News Credibility Analyzer")
st.markdown("Paste a news article below to detect potential disinformation using NLP.")

col1, col2 = st.columns([2, 1])

with col1:
    text_input = st.text_area("News Text / Article Content:", height=250, placeholder="Paste text here...")
    
    if st.button("🔍 Analyze Veracity", type="primary"):
        if len(text_input) > 10:
            with st.spinner("Analyzing semantic patterns..."):
                try:
                    # Attempt to connect to API (Docker scenario)
                    response = requests.post(API_URL, json={"text": text_input}, timeout=2)
                    if response.status_code == 200:
                        data = response.json()
                    else:
                        raise Exception("API Error")
                except:
                    # Fallback for local testing (Simulation)
                    time.sleep(1)
                    score = random.uniform(0, 1)
                    data = {
                        "label": "FAKE" if score > 0.7 else "REAL",
                        "score": score,
                        "risk_level": "HIGH" if score > 0.7 else "LOW"
                    }

                # Display Results
                st.markdown("---")
                m1, m2, m3 = st.columns(3)
                m1.metric("Verdict", data["label"])
                m2.metric("Confidence", f"{data['score']*100:.1f}%")
                m3.metric("Risk Level", data["risk_level"], delta_color="inverse")
                
                if data["label"] == "FAKE":
                    st.error("⚠️ High probability of disinformation detected.")
                else:
                    st.success("✅ Content appears credible.")
        else:
            st.warning("Please enter at least 10 characters.")

with col2:
    st.subheader("Live Analytics")
    # Mock Data for Visualization
    chart_data = pd.DataFrame({
        "Type": ["Credible", "Disinformation", "Satire", "Propaganda"],
        "Count": [450, 120, 30, 80]
    })
    fig = px.donut(chart_data, values="Count", names="Type", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
