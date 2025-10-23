from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crew.agents import evaluate_startup_idea

app = FastAPI(title='Startup Idea Evaluator')

class IdeaIn(BaseModel):
    idea: str
    target_market: str = ''
    competitors: str = ''
    extra_info: str = ''

@app.post('/evaluate')
async def evaluate(idea_in: IdeaIn):
    try:
        report = evaluate_startup_idea({
            'idea': idea_in.idea,
            'target_market': idea_in.target_market,
            'competitors': idea_in.competitors,
            'extra_info': idea_in.extra_info
        })
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
