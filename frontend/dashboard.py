"""
TruthLens Streamlit dashboard — MVP.

Tabs: News Analysis, Trends, Text Analyzer.
Calls backend API (env BACKEND_URL).
"""

from __future__ import annotations

import os

# import streamlit as st
# import requests

# BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def main() -> None:
    """Run Streamlit app with 3 tabs."""
    # st.set_page_config(page_title="TruthLens", layout="wide")
    # tab1, tab2, tab3 = st.tabs(["News Analysis", "Trends", "Text Analyzer"])
    # with tab1: ...
    # with tab2: ...
    # with tab3: ...
    raise NotImplementedError("Streamlit dashboard: implement 3 tabs and API calls")


if __name__ == "__main__":
    main()
