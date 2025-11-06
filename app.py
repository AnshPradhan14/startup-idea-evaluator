import streamlit as st
import json
from crew.agents import evaluate_startup_idea

# ----------- Streamlit Configuration -----------
st.set_page_config(page_title="Startup Idea Evaluator", layout="centered")
st.title("Startup Idea Evaluator with Real-Time Market Insights")

# ----------- Helper Functions -----------
def render_dict_as_bullets(data, indent=0):
    """Recursively render dicts/lists as clean bullet points."""
    output = ""
    spacer = "  " * indent
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                output += f"{spacer}- **{k.capitalize()}**:\n{render_dict_as_bullets(v, indent+1)}"
            else:
                output += f"{spacer}- **{k.capitalize()}**: {v}\n"
    elif isinstance(data, list):
        for i, v in enumerate(data):
            if isinstance(v, (dict, list)):
                output += f"{spacer}- {render_dict_as_bullets(v, indent+1)}"
            else:
                output += f"{spacer}- {v}\n"
    else:
        output += f"{spacer}- {data}\n"
    return output

def render_card(title, content):
    """Display styled section cards with icons and collapsible content."""
    with st.expander(title, expanded=False):
        if isinstance(content, (dict, list)):
            st.markdown(render_dict_as_bullets(content))
        else:
            # Try to parse JSON string
            try:
                parsed = json.loads(content)
                st.markdown(render_dict_as_bullets(parsed))
            except Exception:
                st.markdown(content)

# ----------- User Input Section -----------
idea = st.text_area(
    "Idea Description",
    placeholder="Describe your startup idea here...",
    height=120,
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
)

# ----------- Run Evaluation Button -----------
if st.button("Evaluate Idea"):
    payload = {
        'idea': idea,
        'target_market': market,
        'competitors': competitors,
        'extra_info': extra
    }

    with st.spinner("Evaluating your startup idea..."):
        try:
            report = evaluate_startup_idea(payload)
        except Exception as e:
            st.error(f"Error while running evaluation: {e}")
            import traceback
            st.text_area("Traceback", traceback.format_exc(), height=250)
            report = None

    if report:
        # Optional: Save raw report
        try:
            with open("output_report.json", "w") as f:
                json.dump(report, f, indent=2)
        except Exception:
            pass

        # ----------- Pretty Output Cards -----------
        st.subheader("Detailed Evaluation Report")

        market_data = report.get("market_analysis")
        if market_data:
            render_card("Market Analysis", market_data)

        fin_data = report.get("financial_analysis")
        if fin_data:
            render_card("Financial Analysis", fin_data)

        adv_data = report.get("advisor")
        if adv_data:
            render_card("Advisor Report", adv_data)

        # ----------- Viability Score Section -----------
        with st.expander("📈 Viability Score & Label", expanded=True):
            viability_score = report.get("viability_score")
            viability_label = report.get("viability_label")

            if viability_score is None:
                st.warning("Viability score not found in the report.")
                st.metric("Viability Score", "N/A")
            else:
                try:
                    score_val = float(viability_score)
                except Exception:
                    score_val = 0.0

                if score_val >= 7.5:
                    label = "🟢 Excellent"
                    desc = "Strong market potential and business model."
                elif 5.0 <= score_val < 7.5:
                    label = "🟠 Moderate"
                    desc = "Some risk — improvements recommended."
                else:
                    label = "🔴 Low"
                    desc = "High risk — significant work required."

                st.metric("Viability Score", f"{score_val}/10")
                st.markdown(f"### {label}")
                if viability_label:
                    st.write(f"Provided Label: **{viability_label}**")
                st.caption(desc)

        st.success("Report displayed above. JSON also saved to `output_report.json`.")
