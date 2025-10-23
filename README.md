# Startup Idea Evaluator

A CrewAI-based project for evaluating startup ideas using AI-powered agents. This tool provides structured insights into market potential, financial projections, and overall viability of a startup idea.

---

## 📝 Project Overview

**Project Idea:**  
An AI-powered mobile app that provides personalized meal plans and grocery lists based on a user’s dietary goals, allergies, and local grocery store availability.

**Target Market / Industry:**  
Health-conscious individuals in urban areas, primarily aged 20–40, focusing on fitness and nutrition.

**Competitors:**  
MyFitnessPal, Lifesum, Yazio

**Extra Info:**  
The app integrates with local grocery APIs to auto-generate shopping lists and recommend affordable ingredients from nearby stores.

---

## 🔧 Features

- **Market Analysis Agent:** Evaluates market trends, TAM/TOM estimates, competitors, and customer segments.
- **Financial Analysis Agent:** Generates revenue projections, cost breakdowns, breakeven points, and sensitivity analysis.
- **Advisor Agent:** Provides risks, strengths, weaknesses, actionable recommendations, and a numeric viability score.
- **Gemini LLM Integration:** Uses the Gemini AI model for generating insights from structured prompts.
- **Structured Output:** Generates JSON reports with clear sections for market, financial, and advisory insights.
- **Optional Streamlit Interface:** Visualize results in a clean web-based UI.

---

## 📂 Project Structure

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

## ⚙️ Setup

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

## 🚀 Usage

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

## 🧠 Model Details

- **Gemini Model Used:** gemini-2.5-flash
- **Temperature:** 0.2-0.3 (for deterministic output)
- **Random Seed (Optional):** 42 for reproducible results
- **Features:** Multi-agent CrewAI setup for structured evaluation

---

## 🛠 How It Works

1. **Input Idea** → Provide startup description, market, and competitors.
2. **Market Analysis Agent** → Generates market trends, TAM/TOM estimates, and competitor landscape.
3. **Financial Analysis Agent** → Produces revenue projections, cost breakdowns, and breakeven estimates.
4. **Advisor Agent** → Gives risks, strengths, weaknesses, actionable recommendations, and viability score.
5. **Merge Reports** → Combines outputs from all agents into a structured JSON report.

---

## ⚡ Example Output

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

## 📈 Notes

- LLM outputs are probabilistic. Run multiple evaluations to get an averaged viability score.
- Streamlit interface offers a cleaner visualization for non-technical users.
- Use **lower temperature and fixed seed** for consistent results.

---

## 📦 Dependencies

- Python 3.10+
- Streamlit
- Requests
- CrewAI (or local abstraction)

---

## 📚 References

- [CrewAI Documentation](https://www.crewai.com/docs)
- [Gemini AI API](https://developers.google.com/gemini)
- [Streamlit Documentation](https://docs.streamlit.io)

---

## 📝 License

This project is open-source and licensed under the MIT License.
