MODEL_CARD_TEMPLATE = """
{
  "ModelName": {
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
  "Glossary": {
    "terms": ["Str"]
  },
  "ModelCardAuthors": ["Str"],
  "HowToGetStartedWithTheModel": {
    "examples": ["Str"]
  },
  "Citation": {
    "references": ["Str"]
  },
  "MoreInformation": {
    "links": ["Str"]
  },
  "StructuralInformation": {
    "schema_name": ["Str"],
    "parameter_names": ["Str"],
    "domain": ["Str"],
    "model_type": ["Str"],
    "model_structure": ["Str"],
    "model_parameters": ["Str"]
  }
}
"""

INSTRUCTIONS = """
You are a helpful agent designed to populate a model card containing metadata about a given research paper and its associated model. You may have access to a research paper and a model configuration file. Structural information should come from the model configuration file. \n
Model configurations may be in the form of a petri net, stock and flow, regnet, or other model formats.
You may only have access to either a research paper or model configuration. Do your best to populate the model card with as much information as possible. If you cannot answer the entire query, provide as much information as possible. If there is no answer, use the string "null" as a placeholder. \n
Use the following research paper as a reference: ---PAPER START---{research_paper}---PAPER END--. ---MODEL START-- {amr} ---MODEL END--- Ensure that the output follows the below model card format.\n
TEMPLATE: {model_card_template}\n
Make sure that the following text can be serialized as a JSON object. DO NOT USE ```json``` in the model card header within the json object:\n
{{\n """
