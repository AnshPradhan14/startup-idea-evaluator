import os
import json
import time
from typing import Dict, Any
from services.gemini_client import GeminiClient
from serpapi import GoogleSearch  # <-- fixed import

# ---------------- Gemini Setup ----------------
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise EnvironmentError("Please set GEMINI_API_KEY environment variable.")

llm = GeminiClient(api_key=GEMINI_KEY, model="gemini-2.5-flash")

# ---------------- SerpAPI Setup ----------------
SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
if not SERPAPI_KEY:
    raise EnvironmentError("Please set SERPAPI_KEY environment variable.")

def search_competitors(query, num_results=5):
    """Search for competitors using SerpAPI with proper client usage."""
    try:
        print(f"🔍 Searching for competitors: '{query}'")
        
        search = GoogleSearch({
            "q": query,
            "num": num_results,
            "api_key": SERPAPI_KEY
        })
        
        results = search.get_dict()
        
        if "error" in results:
            print(f"❌ SerpAPI Error: {results['error']}")
            return []
        
        competitors = []
        for r in results.get("organic_results", []):
            competitors.append({
                "title": r.get("title"),
                "link": r.get("link"),
                "snippet": r.get("snippet")
            })
        
        print(f"✅ SerpAPI call successful, found {len(competitors)} results")
        return competitors
        
    except Exception as e:
        print(f"❌ SerpAPI Exception: {str(e)}")
        return []

# ---------------- Market Agent ----------------
def market_agent(context: Dict[str, Any]):
    web_competitors = search_competitors(context["idea"] + " competitors", num_results=5)
    prompt = f"""
You are an expert Market Analyst with 10+ years experience evaluating startups and emerging markets. 

Analyze the following startup idea and provide **a clear, structured market analysis in JSON only**. Include actionable insights, relevant trends, and competitor insights.

STARTUP IDEA: {context['idea']}
TARGET MARKET: {context['target_market']}
WEB COMPETITORS FOUND: {web_competitors}

Your JSON output must include:

1. market_summary:
   - market_size: Estimated market size and growth potential (include sources or reasoning)
   - market_trends: List 3-5 key trends affecting the market
   - market_maturity: Early / Developing / Mature
   - growth_potential: High / Medium / Low, with justification

2. competitors:
   - direct_competitors: List with name, strengths, weaknesses
   - indirect_competitors: List with name and threat level
   - competitive_landscape: Overall assessment of competition intensity

3. customer_segments:
   - primary_segment: Description, size, pain points, willingness_to_pay
   - secondary_segments: List of secondary segments with description and size

4. market_opportunity:
   - opportunity_size: Quantified if possible
   - barriers_to_entry: List key barriers
   - market_timing: Explain why timing is good or bad

Focus only on **objective insights supported by the competitors** and avoid speculative statements.
"""
    resp = llm.generate(prompt)
    return resp
# ---------------- Financial Agent ----------------
def financial_agent(context: Dict[str, Any]):
    prompt = f"""
You are a Financial Analyst specializing in startup financial modeling. 

Analyze the following startup idea and **provide a structured financial report in JSON only**, including realistic numbers and assumptions.

STARTUP IDEA: {context['idea']}
TARGET MARKET: {context['target_market']}
ADDITIONAL CONTEXT: {json.dumps(context, indent=2)}

Your JSON output must include:

1. revenue_projection (for 3 years):
   - revenue, customers, avg_revenue_per_customer
   - growth_rate year-over-year
   - assumptions for projections
   - revenue_model and pricing_strategy

2. costs:
   - operational_costs (personnel, technology, marketing, operations, total) for each year
   - one_time_costs (setup, equipment, legal, total)
   - cost_breakdown explanation

3. breakeven_analysis:
   - breakeven_month
   - breakeven_customers
   - key_metrics: CAC, LTV, LTV:CAC ratio, gross_margin

4. funding_requirements:
   - total_funding_needed
   - breakdown (product, marketing, operations, working capital)
   - runway_months
   - funding_recommendations

5. financial_risks: List top 2-3 risks with mitigation

Ensure assumptions are realistic and justified based on the startup type and market context.
"""
    resp = llm.generate(prompt)
    return resp


# ---------------- Advisor Agent ----------------
def advisor_agent(context: Dict[str, Any]):
    prompt = f"""
You are a Startup Advisor with 15+ years of experience evaluating early-stage companies. 

Using the startup idea, market analysis, and financial analysis provided, **produce a structured advisory report in JSON only**. Be honest, specific, and provide actionable advice.

STARTUP IDEA: {context['idea']}
TARGET MARKET: {context['target_market']}
MARKET ANALYSIS: {json.dumps(context.get('market_out', {}), indent=2)}
FINANCIAL ANALYSIS: {json.dumps(context.get('financial_out', {}), indent=2)}

Your JSON output must include:

1. executive_summary: overall assessment, key opportunities, critical challenges, strategic_position
2. risk_analysis: high_priority_risks, medium_priority_risks, risk_summary
3. strengths_weaknesses: key_strengths, key_weaknesses
4. recommendations: immediate_actions, strategic_recommendations, partnership_opportunities
5. viability_assessment: viability_score, viability_label, scoring_breakdown, key_success_factors, failure_risks
6. next_steps: immediate_priorities, milestones, funding_recommendations
7. market_positioning: unique_value_proposition, competitive_differentiation, target_customer_validation, go_to_market_strategy

Focus on practical, actionable next steps for the founder, and highlight realistic risks and opportunities.
"""
    resp = llm.generate(prompt)
    return resp

# ---------------- Parsing & Merging ----------------
def parse_gemini_response(resp):
    if isinstance(resp, dict) and "candidates" in resp:
        try:
            text = resp["candidates"][0]["content"].get("parts", [{}])[0].get("text", "")
        except Exception:
            text = ""
    else:
        text = str(resp)
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        return {
            "error": "Failed to parse JSON response",
            "raw_response": text[:500] + "..." if len(text) > 500 else text,
            "summary": "Unable to parse structured response from AI model"
        }

def merge_reports(market_out, financial_out, advisor_out, meta):
    market_out = parse_gemini_response(market_out)
    financial_out = parse_gemini_response(financial_out)
    advisor_out = parse_gemini_response(advisor_out)

    report = {
        "idea": meta["idea"],
        "target_market": meta["target_market"],
        "competitors": meta["competitors"],
        "extra_info": meta.get("extra_info", ""),
        "timestamp": meta.get("timestamp", int(time.time())),
        "market_analysis": market_out,
        "financial_analysis": financial_out,
        "advisor": advisor_out,
    }

    if isinstance(report["advisor"], dict):
        viability = report["advisor"].get("viability_assessment", {})
        report["viability_score"] = viability.get("viability_score", 60)
        report["viability_label"] = viability.get("viability_label", "Medium")
        report["advisor"].setdefault("viability_score", report["viability_score"])
        report["advisor"].setdefault("viability_label", report["viability_label"])
    else:
        report["viability_score"] = 60
        report["viability_label"] = "Medium"
        report["advisor"] = {
            "summary": str(report["advisor"]),
            "viability_score": 60,
            "viability_label": "Medium",
            "error": "Failed to parse advisor response"
        }

    return report

# ---------------- Main Evaluation ----------------
def evaluate_startup_idea(payload: Dict[str, Any]):
    meta = {
        "idea": payload.get("idea"),
        "target_market": payload.get("target_market"),
        "competitors": payload.get("competitors"),
        "extra_info": payload.get("extra_info"),
        "timestamp": int(time.time())
    }
    print("→ Running Market Analysis...")
    market_out = market_agent(meta)
    print("→ Running Financial Analysis...")
    financial_out = financial_agent(meta)
    print("→ Running Advisor Analysis...")
    advisor_context = {**meta, "market_out": market_out, "financial_out": financial_out}
    advisor_out = advisor_agent(advisor_context)
    return merge_reports(market_out, financial_out, advisor_out, meta)
