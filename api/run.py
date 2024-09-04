from contextlib import contextmanager
from fastapi import FastAPI, HTTPException
import json
from gollm.openai.tool_utils import model_config_from_document, amodel_card_chain
from gollm.entities import ConfigureModelDocument, ModelCardModel

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
async def configure_model_from_document(input_model: ConfigureModelDocument):
    with handle_http_exception():
        print("Received request to configure model from paper..")
        amr = json.dumps(input_model.amr, separators=(",", ":"))
        research_paper = input_model.research_paper
        response = model_config_from_document(research_paper=research_paper, amr=amr)
        response = {"response": response}
        return json.dumps(response)


@app.post("/model_card")
async def model_card(input_model: ModelCardModel):
    try:
        research_paper = input_model.research_paper
        response = await amodel_card_chain(
            research_paper=research_paper
        )  # Use await here
        response = {"response": response}
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
