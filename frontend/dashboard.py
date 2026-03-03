"""
TruthLens Streamlit dashboard — wide-layout app.

Tabs:
- News Analysis: sentiment pie chart, fake-news risk table.
- Trends: horizontal bar chart of TF-IDF keywords.
- Text Analyzer: free-text analysis.

All data is fetched from the FastAPI backend (default http://localhost:8000).
"""

from __future__ import annotations

import os
from typing import Any, Iterable

import requests
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def _backend_url(path: str) -> str:
    return f"{BACKEND_URL.rstrip('/')}{path}"


def _fetch_json(method: str, path: str, **kwargs: Any) -> dict[str, Any] | None:
    url = _backend_url(path)
    try:
        if method.lower() == "get":
            resp = requests.get(url, timeout=15, **kwargs)
        else:
            resp = requests.post(url, timeout=30, **kwargs)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        st.error(f"Backend request failed: {exc}")
        return None


def _sentiment_distribution(articles: Iterable[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for art in articles:
        sent = art.get("sentiment") or {}
        label = sent.get("label") or "unknown"
        counts[label] = counts.get(label, 0) + 1
    return counts


def run_news_analysis_tab(query: str, language: str, days: int) -> None:
    st.subheader("News Analysis")
    if not query:
        st.info("Введіть тему у сайдбарі й натисніть *Analyze*.")
        return

    with st.spinner("Аналізую новини..."):
        data = _fetch_json(
            "post",
            "/api/news/search",
            json={"query": query, "language": language, "days": days},
        )
    if not data:
        return

    articles = data.get("articles") or []
    st.write(f"Знайдено статей: **{len(articles)}**")

    # Sentiment pie chart
    dist = _sentiment_distribution(articles)
    if dist:
        import plotly.express as px

        pie = px.pie(
            names=list(dist.keys()),
            values=list(dist.values()),
            title="Sentiment distribution of analyzed news",
        )
        st.plotly_chart(pie, use_container_width=True)
    else:
        st.info("Немає даних для побудови діаграми сентименту.")

    # Fake-news risk table
    if articles:
        import pandas as pd

        rows = []
        for art in articles:
            rows.append(
                {
                    "Title": art.get("title"),
                    "Source": art.get("source"),
                    "Fake risk": art.get("fake_news"),
                    "Stars": (art.get("sentiment") or {}).get("stars"),
                    "URL": art.get("url"),
                }
            )
        df = pd.DataFrame(rows)
        st.markdown("### Таблиця ризику фейкових новин")
        st.dataframe(df, use_container_width=True)


def run_trends_tab(query: str, language: str, days: int) -> None:
    st.subheader("Trends")
    if not query:
        st.info("Введіть тему у сайдбарі й натисніть *Analyze*.")
        return

    with st.spinner("Аналізую тренди..."):
        data = _fetch_json(
            "post",
            "/api/trends",
            json={"query": query, "language": language, "days": days},
        )
    if not data:
        return

    keywords = data.get("keywords") or []
    if not keywords:
        st.info("Трендових ключових слів не знайдено.")
        return

    import pandas as pd
    import plotly.express as px

    rows = []
    for kw in keywords:
        if isinstance(kw, dict):
            word = kw.get("keyword") or kw.get("term") or kw.get("word")
            score = kw.get("score")
        else:
            word = str(kw)
            score = None
        if not word:
            continue
        rows.append({"Keyword": word, "Score": score if score is not None else 0.0})

    if not rows:
        st.info("Немає даних для побудови графіка трендів.")
        return

    df = pd.DataFrame(rows)
    df = df.sort_values("Score", ascending=True)
    fig = px.bar(
        df,
        x="Score",
        y="Keyword",
        orientation="h",
        title="TF-IDF keyword importance",
    )
    st.plotly_chart(fig, use_container_width=True)


def run_text_analyzer_tab() -> None:
    st.subheader("Text Analyzer")
    text = st.text_area("Введіть текст для аналізу:", height=200)
    if st.button("Analyze text"):
        if not text.strip():
            st.warning("Будь ласка, введіть текст для аналізу.")
            return
        with st.spinner("Аналізую текст..."):
            data = _fetch_json("post", "/api/analyze", json={"text": text})
        if not data:
            return

        st.markdown("### Результати аналізу")
        sentiment = data.get("sentiment") or {}
        fake_news = data.get("fake_news") or data.get("fake_news_score")
        entities = data.get("entities") or []
        text_length = data.get("text_length")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Sentiment label", sentiment.get("label", "N/A"))
        with col2:
            st.metric("Stars", sentiment.get("stars", "N/A"))
        with col3:
            if isinstance(fake_news, (int, float)):
                st.metric("Fake news risk", f"{fake_news:.2f}")
            else:
                st.metric("Fake news risk", "N/A")

        if text_length is not None:
            st.caption(f"Довжина тексту: {text_length} символів")

        if entities:
            import pandas as pd

            df = pd.DataFrame(entities)
            st.markdown("### Виявлені сутності")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Сутності не виявлено.")


def main() -> None:
    """Run Streamlit app with 3 tabs and sidebar controls."""

    st.set_page_config(page_title="TruthLens", layout="wide")
    st.title("TruthLens — News Intelligence Dashboard")

    # Sidebar controls
    st.sidebar.header("Query settings")
    query = st.sidebar.text_input("Тема / запит для новин та трендів", value="")
    language = st.sidebar.selectbox(
        "Мова аналізу", options=["en", "uk", "de", "fr"], index=0
    )
    days = st.sidebar.slider(
        "Кількість днів для аналізу новин", min_value=1, max_value=30, value=3
    )
    run_analysis = st.sidebar.button("Analyze")

    tab1, tab2, tab3 = st.tabs(["News Analysis", "Trends", "Text Analyzer"])

    if run_analysis:
        with tab1:
            run_news_analysis_tab(query, language, days)
        with tab2:
            run_trends_tab(query, language, days)
    else:
        with tab1:
            st.info("Натисніть *Analyze* у сайдбарі, щоб завантажити аналітику новин.")
        with tab2:
            st.info("Натисніть *Analyze* у сайдбарі, щоб побачити тренди.")

    with tab3:
        run_text_analyzer_tab()


if __name__ == "__main__":
    main()

