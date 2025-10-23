import streamlit as st
import json
from crew.agents import evaluate_startup_idea

st.title("Startup Idea Evaluator with Real-Time Market Data")

idea = st.text_input("Idea Description")
market = st.text_input("Target Market / Industry")
competitors = st.text_input("Known Competitors (comma-separated)")
extra = st.text_area("Extra Info (optional)")

if st.button("Evaluate Idea"):
    payload = {'idea': idea, 'target_market': market, 'competitors': competitors, 'extra_info': extra}
    with st.spinner("Evaluating..."):
        report = evaluate_startup_idea(payload)
    st.subheader("Market Analysis")
    st.json(report["market_analysis"])
    st.subheader("Financial Analysis")
    st.json(report["financial_analysis"])
    st.subheader("Advisor Report")
    st.json(report["advisor"])
