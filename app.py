import streamlit as st
import json
from crew.agents import evaluate_startup_idea

st.set_page_config(page_title="Startup Idea Evaluator", page_icon="🚀", layout="wide")
st.title("🚀 Startup Idea Evaluator")

st.write("Enter your startup idea details below:")

idea = st.text_area("Startup Idea", "An AI-powered nutrition and meal planning app...")
target_market = st.text_input("Target Market", "Health-conscious individuals aged 20–40")
competitors = st.text_input("Competitors", "MyFitnessPal, Lifesum, Yazio")
extra_info = st.text_area("Extra Info (optional)", "Integrates with local grocery APIs...")

if st.button("Evaluate Idea"):
    with st.spinner("Running analysis... please wait ⏳"):
        payload = {
            "idea": idea,
            "target_market": target_market,
            "competitors": competitors,
            "extra_info": extra_info
        }
        report = evaluate_startup_idea(payload)
        st.success("✅ Analysis Complete!")

        st.subheader("📊 Market Analysis")
        st.json(report["market_analysis"])

        st.subheader("💰 Financial Analysis")
        st.json(report["financial_analysis"])

        st.subheader("🧠 Advisor Insights")
        st.json(report["advisor"])

        st.metric("Viability Score", report["advisor"].get("viability_score", 60))
