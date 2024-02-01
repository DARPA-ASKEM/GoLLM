MODEL_CARD_TEMPLATE = """
{
  "ModelName": {
    "model_id": "Unique identifier for the Petri net model.",
    "model_summary": "A brief description of the system or process."
  },
  "ModelDetails": {
    "model_description": "Describe the structure of the model in the paper, including its places, transitions, and arcs. Mention if it can likely be represented in petrinet format.",
    "FundedBy": "If applicable, list the funding sources.",
    "ModelType": "Mathematical / Graphical Model / Other"
  },
  "Uses": {
    "DirectUse": "Explain how the model can be used to analyze or simulate specific systems or processes.",
    "OutOfScopeUse": "Describe scenarios where using the model would be inappropriate or misleading."
  },
  "BiasRisksLimitations": {
    "bias_risks_limitations": "Describe sources of bias and risk based on the research paper"
  },
  "Evaluation": {
    "TestingDataFactorsMetrics": "Describe how the model was validated, e.g., through simulation, comparison with real-world data, etc."
  },
  "TechnicalSpecifications": {
    "model_specs": "Details about the model's complexity, such as the number of places, transitions, parameter count, and arcs."
  },
    "terms": []
  },
  "ModelCardAuthors": [],
  "HowToGetStartedWithTheModel": {
    "examples": ""
  },
  "Citation": {
    "references": []
  },
  "Glossary": {
    "terms": []
  },
  "MoreInformation": {
    "links": []
}
"""
INSTRUCTIONS = """
You are a helpful agent designed to populate a model card containing metadata about a given research paper and its associated model.\n
Use the following research paper as a reference: ---PAPER START---{research_paper}---PAPER END--. Ensure that the output follows the below model card format.\n
TEMPLATE: {model_card_template}\n
BEGIN!\n{{"ModelName":

"""
