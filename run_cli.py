import json
from crew.agents import evaluate_startup_idea, search_competitors

def main():
    print('--- Startup Idea Evaluator CLI ---')

    # Hardcoded payload
    payload = {
        "idea": "An AI-powered mobile app that provides personalized meal plans and grocery lists based on a user’s dietary goals, allergies, and local grocery store availability.",
        "target_market": "Health-conscious individuals in urban areas, primarily aged 20–40, focusing on fitness and nutrition.",
        "competitors": "MyFitnessPal, Lifesum, Yazio",
        "extra_info": "The app integrates with local grocery APIs to auto-generate shopping lists and recommend affordable ingredients from nearby stores."
    }

    # Optional: preview competitors fetched via SerpAPI
    print("\nFetching top competitors and market trends via SerpAPI...")
    try:
        web_competitors = search_competitors(payload["idea"] + " competitors", num_results=5)
        print("Top competitors found on the web:")
        for i, comp in enumerate(web_competitors, 1):
            print(f"{i}. {comp['title']} ({comp['link']})")
    except Exception as e:
        print("Warning: Could not fetch web competitors:", str(e))

    print('\nEvaluating idea via Gemini + SerpAPI...\n')
    report = evaluate_startup_idea(payload)

    # Save structured JSON output
    out_path = 'output_report.json'
    with open(out_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f'\nReport written to {out_path} — open the file to review the structured output.')

if __name__ == '__main__':
    main()
