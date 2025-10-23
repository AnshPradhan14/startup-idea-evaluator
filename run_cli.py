import json
from crew.agents import evaluate_startup_idea

def main():
    print('--- Startup Idea Evaluator CLI ---')

    payload = {
        "idea": "An AI-powered mobile app that provides personalized meal plans and grocery lists based on a user’s dietary goals, allergies, and local grocery store availability.",
        "target_market": "Health-conscious individuals in urban areas, primarily aged 20–40, focusing on fitness and nutrition.",
        "competitors": "MyFitnessPal, Lifesum, Yazio",
        "extra_info": "The app integrates with local grocery APIs to auto-generate shopping lists and recommend affordable ingredients from nearby stores."
    }

    print('\nEvaluating... this calls Gemini via the configured GEMINI_API_KEY.\n')
    report = evaluate_startup_idea(payload)

    out_path = 'output_report.json'
    with open(out_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f'Report written to {out_path} — open the file to review the structured output.')

if __name__ == '__main__':
    main()
