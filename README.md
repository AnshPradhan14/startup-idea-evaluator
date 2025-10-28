# Startup Idea Evaluator

A CrewAI-based project that evaluates startup ideas across Market, Financial, and Strategic dimensions using Google Gemini and SerpAPI for real-world insights.

This project helps founders, students, and investors quickly understand the feasibility, competitive landscape, and financial potential of any business idea — all from a single interface.

---

## Overview

The Startup Idea Evaluator is an intelligent agent-based system that uses LLMs (Gemini) and live web data (SerpAPI) to provide an objective, multi-layered evaluation of a startup concept.

Each idea is analyzed through three expert AI agents:

1. Market Analyst Agent – Evaluates market trends, customer segments, and real competitors.
2. Financial Analyst Agent – Builds financial projections and breakeven models.
3. Startup Advisor Agent – Assesses strategic fit, risks, and overall viability.

It returns a structured JSON report and a Streamlit web interface for interactive exploration.

---


## Features

| Category                      | Description                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------ |
| **Market Analysis**        | Identifies trends, customer segments, and competitive landscape using SerpAPI. |
| **Financial Analysis**     | Generates financial forecasts, pricing strategies, and funding requirements.   |
| **Advisory Report**     | Provides actionable insights, risks, and strategic recommendations.            |
| **Real-World Data**        | Integrates **SerpAPI** to fetch up-to-date competitors and market signals.     |
| **AI-Driven Evaluation**   | Uses **Gemini 2.5 Flash** for advanced reasoning and scoring.                  |
| **Structured JSON Output** | Produces clean, structured data ready for dashboards or reports.               |
| **Streamlit Frontend**     | Interactive form for entering and evaluating startup ideas dynamically.        |


---

## Project Structure

```
startup-idea-evaluator/
├─ .venv/                    # Python virtual environment
├─ crew/
│  ├─ agents.py              # Market, Financial, Advisor agents
├─ services/
│  ├─ gemini_client.py       # Gemini API wrapper
├─ run_cli.py                # Command-line interface
├─ app.py                    # Streamlit app interface
├─ output_report.json        # Generated report
├─ README.md                 # Project documentation
└─ requirements.txt          # Python dependencies
```

---

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd startup-idea-evaluator
```

2. Create a Python virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
- **Windows:**
```bash
.venv\Scripts\activate
```
- **Mac/Linux:**
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set your Gemini API key:
```bash
export GEMINI_API_KEY=<your_key>    # Mac/Linux
set GEMINI_API_KEY=<your_key>       # Windows
```

---

## Usage

### Command-Line Interface
Run the CLI to evaluate a startup idea:
```bash
python run_cli.py
```
Follow the prompts to enter:
- Idea description
- Target market / industry
- Competitors
- Extra information (optional)

The report will be generated as `output_report.json`.

### Streamlit Interface
Run the Streamlit app:
```bash
streamlit run app.py
```
- Input your startup idea details in the web interface.
- Click **Evaluate** to view a structured report with market analysis, financial analysis, and advisor recommendations.

---

## Model Details

- **Gemini Model Used:** gemini-2.5-flash
- **Temperature:** 0.2-0.3 (for deterministic output)
- **Random Seed (Optional):** 42 for reproducible results
- **Features:** Multi-agent CrewAI setup for structured evaluation

---

## How It Works

1. **Input Idea** → Provide startup description, market, and competitors.
2. **Market Analysis Agent** → Generates market trends, TAM/TOM estimates, and competitor landscape.
3. **Financial Analysis Agent** → Produces revenue projections, cost breakdowns, and breakeven estimates.
4. **Advisor Agent** → Gives risks, strengths, weaknesses, actionable recommendations, and viability score.
5. **Merge Reports** → Combines outputs from all agents into a structured JSON report.

---

## Example Output

```json
{
  "idea": "AI-powered meal planner",
  "target_market": "Health-conscious urban users",
  "competitors": "MyFitnessPal, Lifesum, Yazio",
  "market_analysis": {...},
  "financial_analysis": {...},
  "advisor": {
    "risks": [...],
    "strengths": [...],
    "weaknesses": [...],
    "recommendations": [...],
    "viability_score": 68,
    "viability_label": "Medium"
  }
}
```

---

## Notes

- LLM outputs are probabilistic. Run multiple evaluations to get an averaged viability score.
- Streamlit interface offers a cleaner visualization for non-technical users.
- Use **lower temperature and fixed seed** for consistent results.

---

## Dependencies

- Python 3.10+
- Streamlit
- Requests
- CrewAI (or local abstraction)

---

## References

- [CrewAI Documentation](https://www.crewai.com/docs)
- [Gemini AI API](https://developers.google.com/gemini)
- [Streamlit Documentation](https://docs.streamlit.io)

---

## License

This project is open-source and licensed under the MIT License.
