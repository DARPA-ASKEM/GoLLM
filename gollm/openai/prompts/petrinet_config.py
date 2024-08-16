PETRINET_PROMPT = """
You are a helpful agent designed to find multiple model configurations for a given Petri net model of various conditions described in a given research paper.

Use the following Petri net json file as a reference:

--START PETRI NET MODEL JSON--
{petrinet}
--END PETRI NET MODEL JSON--

Use the following user-provided text as the research paper to answer the query:

--START USER-PROVIDED TEXT--
{research_paper}
--END USER-PROVIDED TEXT--

Assume that there are multiple conditions described in the user-provided text. For each condition, create a model configuration.
Be sure to extract parameter values and initial values from the user-provided text and do not use the default values from the Petri net model.
Be sure to use consistent naming conventions for the conditions. Instead of 'condition_1' and 'condition_2', use names that are descriptive of the conditions.

For each condition, create a model configuration following the instructions below:
	- Create a value for `name` and `description` from the user supplied text.
	- For the description, provide long-form description of the condition. If the description can not be created from the user provided text, set it to an empty string "".
	- `model_id` should reference the id of the Petri net model.
	- For each initial in the Petri net model ODE semantics, create a initial semantic object with the following fields:
		- `target` should reference the id of the initial variable
		- `source` should reference the title or file name of the research paper
		- `type` should be set to "initial"
		- `expression` should be written in LaTeX format
		- `expression_mathml` should be written in MathML format
	    - For `expression` and `expression_mathml`, Ensure both are valid and represent the same unit. If the unit is not found or not valid, omit the units field.
	- For each parameter in the Petri net model ODE semantics, create a parameter semantic object with the following fields:
		- `reference_id` should reference the id of the parameter.
		- `source` should reference the title or file name of the research paper.
		- `type` should be set to "parameter".
		- If the extracted parameter semantic value is a single constant value, set the parameter `value` to the constant value and set `type` to "constant".
		- If the extracted parameter semantic value is a distribution with a maximum and minumum value, set `type` to "uniform" and populate the `minimum` and `maximum` fields.

Do not respond in full sentences, only create a json object that satisfies the json schema specified in the response format.

Answer:
"""
