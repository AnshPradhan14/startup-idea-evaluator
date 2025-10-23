"""CrewAI-based crew definition for the three specialized agents and orchestration.
This module demonstrates an idiomatic CrewAI setup (agents -> crew -> run).

Important: this code assumes you have the `crewai` Python package installed and that
CrewAI can be configured to use a custom LLM provider. We use a Gemini adapter in
`services/gemini_client.py` for demonstration.
"""

from typing import Dict, Any
import time
import json
import os

from services.gemini_client import GeminiClient

# Load Gemini key and initialize client
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", None)
if not GEMINI_KEY:
    raise EnvironmentError("Please set GEMINI_API_KEY environment variable.")

llm = GeminiClient(api_key=GEMINI_KEY, model="gemini-2.5-flash")

# ----------------------------- #
#           AGENTS              #
# ----------------------------- #

def market_agent(context: Dict[str, Any]):
    prompt = f"""
You are a **Market Analyst AI**.

Analyze the following startup idea and provide a strictly valid JSON response with these keys:
- **market_summary**: A concise paragraph summarizing the current market context and opportunity.
- **key_trends**: A list (array) of 3–5 current or emerging market trends relevant to this idea.
- **competitors**: A list of competitor companies, each with fields `name`, `strengths`, and `weaknesses`.
- **customer_segments**: A short list of main target customer profiles or demographics.
- **tam_tom_estimates**: Object with numeric or textual TAM (Total Addressable Market) and TOM (Target Obtainable Market) values.

Startup Context:
{json.dumps(context, indent=2)}

⚠️ Return **only valid JSON** — no Markdown, no backticks, no explanations.
"""
    return llm.generate(prompt)


def financial_agent(context: Dict[str, Any]):
    prompt = f"""
You are a **Financial Analyst AI**.

Analyze the following startup idea and provide a strictly valid JSON response with these keys:
- **revenue_projection**: 3-year projection as an object with `year_1`, `year_2`, and `year_3` revenues (in USD or INR).
- **costs**: An object with approximate annual cost breakdowns (`development`, `marketing`, `operations`, etc.).
- **breakeven_analysis**: A short summary of when breakeven could occur and key assumptions.
- **sensitivity_analysis**: How profitability changes if CAC (Customer Acquisition Cost) or churn changes by ±20%.

Startup Context:
{json.dumps(context, indent=2)}

⚠️ Return **only valid JSON** — no Markdown, no backticks, no commentary.
"""
    return llm.generate(prompt)


def advisor_agent(context: Dict[str, Any]):
    prompt = f"""
You are an **Advisor AI**.

Given the startup idea, market analysis, and financial analysis, provide a strictly valid JSON response with these keys:
- **strengths**: List of 3–5 key strengths of this startup.
- **weaknesses**: List of 3–5 weaknesses or challenges.
- **risks**: List of top 3–5 potential risks or uncertainties.
- **recommendations**: 5 actionable, specific suggestions to improve success chances.
- **viability_label**: One of ["High", "Medium", "Low"].
- **viability_score**: A numeric score between 0–100.

Context:
{json.dumps(context, indent=2)}

⚠️ Return **only valid JSON** — no Markdown, no backticks, no text outside JSON.
"""
    return llm.generate(prompt)


# ----------------------------- #
#        RESPONSE HELPERS       #
# ----------------------------- #

def parse_gemini_response(resp):
    """Extracts the model-generated text from Gemini API response and converts it to a Python dict if possible."""
    if isinstance(resp, dict) and "candidates" in resp:
        try:
            text = resp["candidates"][0]["content"].get("parts", [{}])[0].get("text", "")
        except Exception:
            text = ""
    else:
        text = str(resp)

    text = text.strip().replace("```json", "").replace("```", "")

    try:
        parsed = json.loads(text)
        return parsed
    except Exception:
        return {"summary": text}


def merge_reports(market_out, financial_out, advisor_out, meta):
    market_out = parse_gemini_response(market_out)
    financial_out = parse_gemini_response(financial_out)
    advisor_out = parse_gemini_response(advisor_out)

    report = {
        "idea": meta["idea"],
        "target_market": meta["target_market"],
        "competitors": meta["competitors"],
        "extra_info": meta.get("extra_info", ""),
        "market_analysis": market_out,
        "financial_analysis": financial_out,
        "advisor": advisor_out,
    }

    # Ensure viability score
    if isinstance(report["advisor"], dict):
        report["advisor"].setdefault("viability_score", 60)
        report["advisor"].setdefault("viability_label", "Medium")
    else:
        report["advisor"] = {
            "summary": str(report["advisor"]),
            "viability_score": 60,
            "viability_label": "Medium",
        }

    return report


# ----------------------------- #
#        MAIN ORCHESTRATION     #
# ----------------------------- #

def evaluate_startup_idea(payload: Dict[str, Any]):
    meta = {
        "idea": payload.get("idea"),
        "target_market": payload.get("target_market"),
        "competitors": payload.get("competitors"),
        "extra_info": payload.get("extra_info"),
        "timestamp": int(time.time()),
    }

    print("→ Running Market Analysis...")
    market_out = market_agent(meta)

    print("→ Running Financial Analysis...")
    financial_out = financial_agent(meta)

    print("→ Running Advisor Evaluation...")
    advisor_context = {**meta, "market_out": market_out, "financial_out": financial_out}
    advisor_out = advisor_agent(advisor_context)

    return merge_reports(market_out, financial_out, advisor_out, meta)
