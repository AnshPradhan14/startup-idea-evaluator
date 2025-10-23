import os
import json
import time
from typing import Dict, Any
from services.gemini_client import GeminiClient
from serpapi import GoogleSearch



# Gemini setup
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise EnvironmentError("Please set GEMINI_API_KEY environment variable.")

llm = GeminiClient(api_key=GEMINI_KEY, model="gemini-2.5-flash")

# SerpAPI setup
SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
if not SERPAPI_KEY:
    raise EnvironmentError("Please set SERPAPI_KEY environment variable.")

def search_competitors(query, num_results=5):
    search = GoogleSearch({
        "q": query,
        "num": num_results,
        "api_key": os.environ.get("SERPAPI_API_KEY")
    })
    results = search.get_dict()
    competitors = []
    for r in results.get("organic_results", []):
        competitors.append({
            "title": r.get("title"),
            "link": r.get("link"),
            "snippet": r.get("snippet")
        })
    return competitors


def market_agent(context: Dict[str, Any]):
    web_competitors = search_competitors(context["idea"] + " competitors", num_results=5)
    prompt = f"""
    You are an expert Market Analyst specializing in startup evaluation. Analyze the following startup idea and provide comprehensive market insights.

    STARTUP IDEA: {context['idea']}
    TARGET MARKET: {context['target_market']}
    WEB COMPETITORS FOUND: {web_competitors}

    Please provide a detailed market analysis in the following JSON structure:

    {{
        "market_summary": {{
            "market_size": "Estimated market size and growth potential",
            "market_trends": ["Trend 1", "Trend 2", "Trend 3"],
            "market_maturity": "Early/Developing/Mature",
            "growth_potential": "High/Medium/Low with reasoning"
        }},
        "competitors": {{
            "direct_competitors": [
                {{"name": "Company Name", "strength": "Key strength", "weakness": "Key weakness"}}
            ],
            "indirect_competitors": [
                {{"name": "Company Name", "threat_level": "High/Medium/Low"}}
            ],
            "competitive_landscape": "Overall assessment of competition intensity"
        }},
        "customer_segments": {{
            "primary_segment": {{
                "description": "Main target customers",
                "size": "Estimated segment size",
                "pain_points": ["Pain point 1", "Pain point 2"],
                "willingness_to_pay": "High/Medium/Low"
            }},
            "secondary_segments": [
                {{"description": "Secondary customer group", "size": "Estimated size"}}
            ]
        }},
        "market_opportunity": {{
            "opportunity_size": "Quantified opportunity if possible",
            "barriers_to_entry": ["Barrier 1", "Barrier 2"],
            "market_timing": "Why now is good/bad timing"
        }}
    }}

    Focus on actionable insights and be specific with your analysis. Use data from the web competitors when available.
    """
    resp = llm.generate(prompt)
    return resp

def financial_agent(context: Dict[str, Any]):
    prompt = f"""
    You are an expert Financial Analyst specializing in startup financial modeling. Analyze the following startup idea and provide comprehensive financial projections.

    STARTUP IDEA: {context['idea']}
    TARGET MARKET: {context['target_market']}
    ADDITIONAL CONTEXT: {json.dumps(context, indent=2)}

    Please provide a detailed financial analysis in the following JSON structure:

    {{
        "revenue_projection": {{
            "year_1": {{
                "revenue": 0,
                "customers": 0,
                "avg_revenue_per_customer": 0,
                "assumptions": "Key assumptions for year 1"
            }},
            "year_2": {{
                "revenue": 0,
                "customers": 0,
                "avg_revenue_per_customer": 0,
                "growth_rate": "0%",
                "assumptions": "Key assumptions for year 2"
            }},
            "year_3": {{
                "revenue": 0,
                "customers": 0,
                "avg_revenue_per_customer": 0,
                "growth_rate": "0%",
                "assumptions": "Key assumptions for year 3"
            }},
            "revenue_model": "Description of how revenue is generated",
            "pricing_strategy": "Recommended pricing approach"
        }},
        "costs": {{
            "operational_costs": {{
                "year_1": {{
                    "personnel": 0,
                    "technology": 0,
                    "marketing": 0,
                    "operations": 0,
                    "total": 0
                }},
                "year_2": {{
                    "personnel": 0,
                    "technology": 0,
                    "marketing": 0,
                    "operations": 0,
                    "total": 0
                }},
                "year_3": {{
                    "personnel": 0,
                    "technology": 0,
                    "marketing": 0,
                    "operations": 0,
                    "total": 0
                }}
            }},
            "one_time_costs": {{
                "initial_setup": 0,
                "equipment": 0,
                "legal": 0,
                "total": 0
            }},
            "cost_breakdown": "Detailed explanation of major cost categories"
        }},
        "breakeven_analysis": {{
            "breakeven_month": "Month when breakeven is achieved",
            "breakeven_customers": "Number of customers needed to breakeven",
            "cac_sensitivity": {{
                "current_cac": 0,
                "impact_10_percent_increase": "Impact on profitability",
                "impact_20_percent_increase": "Impact on profitability"
            }},
            "key_metrics": {{
                "customer_acquisition_cost": 0,
                "lifetime_value": 0,
                "lifetime_value_to_cac_ratio": 0,
                "gross_margin": "0%"
            }}
        }},
        "funding_requirements": {{
            "total_funding_needed": 0,
            "funding_breakdown": {{
                "product_development": 0,
                "marketing": 0,
                "operations": 0,
                "working_capital": 0
            }},
            "runway_months": "Months of runway with current funding",
            "funding_recommendations": "Recommended funding strategy"
        }},
        "financial_risks": [
            "Risk 1 with mitigation strategy",
            "Risk 2 with mitigation strategy"
        ]
    }}

    Make realistic assumptions based on the startup idea and market context. Provide specific numbers where possible and explain your reasoning.
    """
    resp = llm.generate(prompt)
    return resp

def advisor_agent(context: Dict[str, Any]):
    prompt = f"""
    You are an expert Startup Advisor with extensive experience in evaluating early-stage companies. Analyze the following startup idea along with market and financial data to provide comprehensive strategic guidance.

    STARTUP IDEA: {context['idea']}
    TARGET MARKET: {context['target_market']}
    MARKET ANALYSIS: {json.dumps(context.get('market_out', {}), indent=2)}
    FINANCIAL ANALYSIS: {json.dumps(context.get('financial_out', {}), indent=2)}

    Please provide a comprehensive advisory assessment in the following JSON structure:

    {{
        "executive_summary": {{
            "overall_assessment": "High-level summary of the startup's potential",
            "key_opportunities": ["Opportunity 1", "Opportunity 2"],
            "critical_challenges": ["Challenge 1", "Challenge 2"],
            "strategic_position": "How well positioned this startup is in the market"
        }},
        "risk_analysis": {{
            "high_priority_risks": [
                {{
                    "risk": "Risk description",
                    "impact": "High/Medium/Low",
                    "probability": "High/Medium/Low",
                    "mitigation": "Recommended mitigation strategy"
                }}
            ],
            "medium_priority_risks": [
                {{
                    "risk": "Risk description",
                    "impact": "High/Medium/Low",
                    "probability": "High/Medium/Low",
                    "mitigation": "Recommended mitigation strategy"
                }}
            ],
            "risk_summary": "Overall risk assessment and key concerns"
        }},
        "strengths_weaknesses": {{
            "key_strengths": [
                {{
                    "strength": "Strength description",
                    "impact": "How this strength benefits the startup",
                    "sustainability": "How sustainable this advantage is"
                }}
            ],
            "key_weaknesses": [
                {{
                    "weakness": "Weakness description",
                    "impact": "How this weakness hurts the startup",
                    "improvement": "How to address this weakness"
                }}
            ]
        }},
        "recommendations": {{
            "immediate_actions": [
                {{
                    "action": "Specific actionable recommendation",
                    "priority": "High/Medium/Low",
                    "timeline": "When to implement",
                    "expected_impact": "Expected outcome"
                }}
            ],
            "strategic_recommendations": [
                {{
                    "recommendation": "Strategic recommendation",
                    "rationale": "Why this is important",
                    "implementation": "How to implement"
                }}
            ],
            "partnership_opportunities": [
                "Potential partnership or collaboration opportunity"
            ]
        }},
        "viability_assessment": {{
            "viability_score": 75,
            "viability_label": "High/Medium/Low",
            "scoring_breakdown": {{
                "market_opportunity": 0,
                "competitive_advantage": 0,
                "financial_feasibility": 0,
                "team_execution": 0,
                "market_timing": 0
            }},
            "key_success_factors": [
                "Factor 1 that will determine success",
                "Factor 2 that will determine success"
            ],
            "failure_risks": [
                "Primary risk that could lead to failure"
            ]
        }},
        "next_steps": {{
            "immediate_priorities": [
                "Priority 1 to focus on first",
                "Priority 2 to focus on first"
            ],
            "milestones": [
                {{
                    "milestone": "Specific milestone to achieve",
                    "timeline": "When to achieve it",
                    "success_metrics": "How to measure success"
                }}
            ],
            "funding_recommendations": "Specific funding advice and timeline"
        }},
        "market_positioning": {{
            "unique_value_proposition": "Clear, compelling value proposition",
            "competitive_differentiation": "How to stand out from competitors",
            "target_customer_validation": "How to validate customer demand",
            "go_to_market_strategy": "Recommended approach to market entry"
        }}
    }}

    Provide specific, actionable advice based on the market and financial analysis. Be honest about challenges while highlighting opportunities. Focus on practical next steps the founder can take.
    """
    resp = llm.generate(prompt)
    return resp

def parse_gemini_response(resp):
    """Parse Gemini response and extract JSON content with better error handling."""
    if isinstance(resp, dict) and "candidates" in resp:
        try:
            text = resp["candidates"][0]["content"].get("parts", [{}])[0].get("text", "")
        except Exception:
            text = ""
    else:
        text = str(resp)
    
    # Try to extract JSON from the response
    try:
        # First, try to parse the entire response as JSON
        return json.loads(text)
    except json.JSONDecodeError:
        # If that fails, try to find JSON within the text
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # If all else fails, return a structured error response
        return {
            "error": "Failed to parse JSON response",
            "raw_response": text[:500] + "..." if len(text) > 500 else text,
            "summary": "Unable to parse structured response from AI model"
        }

def merge_reports(market_out, financial_out, advisor_out, meta):
    """Merge all agent outputs into a comprehensive report with better error handling."""
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

    # Ensure viability score exists with better fallback handling
    if isinstance(report["advisor"], dict):
        # Extract viability from the new structured format
        viability_assessment = report["advisor"].get("viability_assessment", {})
        report["viability_score"] = viability_assessment.get("viability_score", 60)
        report["viability_label"] = viability_assessment.get("viability_label", "Medium")
        
        # Ensure backward compatibility
        report["advisor"].setdefault("viability_score", report["viability_score"])
        report["advisor"].setdefault("viability_label", report["viability_label"])
    else:
        # Fallback for parsing errors
        report["viability_score"] = 60
        report["viability_label"] = "Medium"
        report["advisor"] = {
            "summary": str(report["advisor"]), 
            "viability_score": 60, 
            "viability_label": "Medium",
            "error": "Failed to parse advisor response"
        }

    return report

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
