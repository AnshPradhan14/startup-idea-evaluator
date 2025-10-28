import streamlit as st
import json
from crew.agents import evaluate_startup_idea

st.set_page_config(page_title="Startup Idea Evaluator", layout="centered")
st.title("Startup Idea Evaluator with Real-Time Market Data")

# --- Inputs (with dynamic resizing) ---
idea = st.text_area(
    "Idea Description",
    placeholder="Describe your startup idea here...",
    height=120,
    key="idea_input"
)

market = st.text_input(
    "Target Market / Industry",
    placeholder="e.g. Health-conscious urban individuals, aged 20–40..."
)

competitors = st.text_input(
    "Known Competitors (comma-separated)",
    placeholder="e.g. MyFitnessPal, Lifesum, Yazio"
)

extra = st.text_area(
    "Extra Info (optional)",
    placeholder="Any additional context, such as unique selling points or technologies used...",
    height=100,
    key="extra_info"
)


if st.button("Evaluate Idea"):
    payload = {
        'idea': idea,
        'target_market': market,
        'competitors': competitors,
        'extra_info': extra
    }

    # call agents (wrapped in try/except to surface errors)
    with st.spinner("Evaluating... this calls Gemini + SerpAPI..."):
        try:
            report = evaluate_startup_idea(payload)
        except Exception as e:
            st.error(f"Error while running evaluation: {e}")
            # show exception + hint to console
            import traceback
            st.text_area("Traceback", traceback.format_exc(), height=250)
            report = None

    if report:
        # Save raw report for inspection (optional)
        try:
            with open("output_report.json", "w") as f:
                json.dump(report, f, indent=2)
        except Exception:
            pass

        # ---- Market Analysis (dropdown) ----
        with st.expander("🌍 Market Analysis", expanded=False):
            market_data = report.get("market_analysis")
            if market_data is None:
                st.warning("No market_analysis key found in report.")
                st.write("Raw report (market_analysis missing):")
                st.json(report)  # debugging fallback
            else:
                # If market_data is already JSON/dict -> show prettily; otherwise show raw text
                if isinstance(market_data, (dict, list)):
                    st.json(market_data)
                else:
                    # sometimes the LLM returns a string with JSON — show text and try parse
                    st.write(market_data)
                    try:
                        parsed = json.loads(market_data)
                        st.markdown("**Parsed JSON:**")
                        st.json(parsed)
                    except Exception:
                        pass

        # ---- Financial Analysis (dropdown) ----
        with st.expander("💰 Financial Analysis", expanded=False):
            fin_data = report.get("financial_analysis")
            if fin_data is None:
                st.warning("No financial_analysis key found in report.")
                st.write("Raw report (financial_analysis missing):")
                st.json(report)
            else:
                if isinstance(fin_data, (dict, list)):
                    st.json(fin_data)
                else:
                    st.write(fin_data)
                    try:
                        st.json(json.loads(fin_data))
                    except Exception:
                        pass

        # ---- Advisor Report (dropdown) ----
        with st.expander("🧑‍🏫 Advisor Report", expanded=False):
            adv_data = report.get("advisor")
            if adv_data is None:
                st.warning("No advisor key found in report.")
                st.write("Raw report (advisor missing):")
                st.json(report)
            else:
                if isinstance(adv_data, (dict, list)):
                    st.json(adv_data)
                else:
                    st.write(adv_data)
                    try:
                        st.json(json.loads(adv_data))
                    except Exception:
                        pass

        # ---- Viability Score (dropdown) ----
        with st.expander("📈 Viability Score & Label", expanded=True):
            # Try several locations where viability might exist for backward-compatibility
            viability_score = None
            viability_label = None

            # common placements
            if isinstance(report.get("viability_score"), (int, float)):
                viability_score = report.get("viability_score")
            elif isinstance(report.get("advisor"), dict) and report["advisor"].get("viability_score") is not None:
                viability_score = report["advisor"].get("viability_score")

            # sometimes score is string; try to coerce
            if viability_score is None:
                vs = report.get("viability_score") or (report.get("advisor") and report["advisor"].get("viability_score"))
                if isinstance(vs, str):
                    try:
                        viability_score = float(vs)
                    except Exception:
                        viability_score = None

            # label (try a few keys)
            if report.get("viability_label"):
                viability_label = report.get("viability_label")
            elif isinstance(report.get("advisor"), dict):
                viability_label = report["advisor"].get("viability_label")

            # Default fallback
            if viability_score is None:
                st.warning("Viability score not found. Showing default placeholder.")
                st.write("Viability score missing in report structure.")
                st.metric("Viability Score", "N/A")
            else:
                # Normalize 0-100
                try:
                    score_val = float(viability_score)
                except Exception:
                    score_val = 0.0

                # choose color label
                if score_val >= 75:
                    label = "🟢 Excellent"
                    desc = "Strong market potential and business model."
                elif 50 <= score_val < 75:
                    label = "🟠 Moderate"
                    desc = "Some risk — improvements recommended."
                else:
                    label = "🔴 Low"
                    desc = "High risk — significant work required."

                st.metric(label="Viability Score", value=f"{score_val}/100")
                st.markdown(f"### {label}")
                if viability_label:
                    st.write(f"Provided label: **{viability_label}**")
                st.caption(desc)

        st.success("Report displayed above. JSON also saved to `output_report.json`.")
