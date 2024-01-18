from contextlib import contextmanager
from fastapi import FastAPI, HTTPException
import json
from core.openai.tool_utils import _model_config_chain, _model_card_chain
from core.entities import ConfigureModel, ModelCardModel

app = FastAPI()

@contextmanager
def handle_http_exception():
    # Handles arbitrary server errors. TODO: add more specific error handling.
    try:
        yield
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "GoLLM API is running!"}

@app.post("/configure")
async def configure_model(input_model: ConfigureModel):
    with handle_http_exception():
        print('Received request to configure model from paper..')
        amr = json.dumps(input_model.amr, separators=(',', ':'))
        research_paper = input_model.research_paper
        response = _model_config_chain(research_paper=research_paper, amr=amr)
        response = {"response": response}
        return json.dumps(response)

@app.post("/model_card")
async def model_card(input_model: ModelCardModel):
    with handle_http_exception():
        research_paper = input_model.research_paper
        response = _model_card_chain(research_paper=research_paper)
        response = {"response": response}
        return json.dumps(response)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
