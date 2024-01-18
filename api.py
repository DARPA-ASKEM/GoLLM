from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import Dict
from core.openai.tool_utils import _model_config_chain

app = FastAPI()

class InputModel(BaseModel):
    ## Use this an input validator.
    research_paper: str
    amr: Dict # expects AMR in JSON format

@app.post("/configure")
async def process_input(input_model: InputModel):
    try:
        # Convert AMR to JSON string
        amr = json.dumps(input_model.amr, separators=(',', ':'))
        research_paper = input_model.research_paper

        # Call the model configuration chain
        response = _model_config_chain(research_paper=research_paper, amr=amr)
        response = {"response": response}
        return json.dumps(response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
