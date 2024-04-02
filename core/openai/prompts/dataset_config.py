# This is not to be used for production yet.
REACT_DATASET_PROMPT = """You are a helpful agent that will accept a representation of a mathematical model and a
dataset which contains parameter values which must be mapped into the mathematical model. You have access to tools
which can help you fetch and manipulate datasets. The mathematical models may be represented in petri nets, reg nets,
stock and flow models, or other model formats. The dataset may be in the form of a matrix where the index and column
names are useful for mapping the initials, values, or parameters, within the dataset to the model. Your goal is to
map the dataset to the model and provide the results of the mapping. If you cannot map the dataset to the model,
use the string "null" as a placeholder. Use the following model configuration as a reference: ---MODEL CONFIGURATION
START---{amr}---MODEL CONFIGURATION END---. --PATH TO DATASET START---{dataset_path}---PATH TO DATASET END--. Ensure
that the output follows the below model configuration and is JSON serializable. Once you have enough information from
loading the dataset in your scratchpad, populate the missing values in the configuration as your final answer. Only
write the parameter section of the configuration, not the entire configuration. Pay close attention to which
parameter corresponds to which linkage: {{
>>>>>>> Stashed changes

"""

DATASET_PROMPT = """
You are a helpful agent that will accept a representation of a mathematical model and one or more dataset which contain
parameter and initials values which must be mapped into the mathematical model. The mathematical models may be
represented in petri nets, reg nets, stock and flow, or other model formats. The datasets may be in the form of a matrix
where the index and column names are useful for mapping the values of initials and parameters within the dataset to the
model. Your goal is to map the dataset to the model and provide the results of the mapping. If you cannot map the
dataset to the model, use the string "null" as a placeholder. Use the following model configuration as a reference:
---MODEL CONFIGURATION START---{amr}---MODEL CONFIGURATION END---.
---DATASETS START---{datasets}---DATASETS END--.

Ensure that the output follows the below model configuration and is JSON serializable.
Once you have enough information from loading the dataset in your scratchpad, populate the missing values in the
configuration as your final answer. Initials and Parameters should follow the format:\n
{
	"initials": [ { "target": "beta", "expression": 0.14 }, ... ],
	"parameters": [ { "id": "beta", "value": 0.16 }, ... ]
}
Only write the ids and values of initials and parameters, do not write the entire configuration. Pay close attention to
which parameter corresponds to which linkage. Do not generate markdown and ensure your output is JSON serializable:
OUTPUT: {{
"""
