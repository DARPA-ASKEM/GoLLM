PETRINET_PROMPT = """
You are a helpful agent designed to find model configurations for a given petri net model file and a given research paper describing the mathematical model.

Use the following petri net json file as a reference:

--START PETRI NET MODEL JSON--
{petrinet}
--END PETRI NET MODEL JSON--

Assume that there are multiple model configurations in the user provided text for different conditions. Be sure to use consistent naming conventions for the conditions. Instead of 'condition_1' and 'condition_2'.. use names that are descriptive of the conditions.

For each model configuration only use initial variables and parameters found in the reference Petri net model. Unsure that you follow the instructions below:
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
		- If the extracted parameter value is a constant, set the parameter `value` to the constant value and set `type` to "constant".
		- If the extracted parameter value is a distribution, set the distribution type using 'name' and from the following probability distribution ontology JSON and populate the `minimum` and `maximum` fields.

--START PROBABILITY DISTRIBUTION ONTOLOGY JSON--
{pb}
--END PROBABILITY DISTRIBUTION ONTOLOGY JSON--

Use the following text body to answer the query:

--START USER PROVIDED TEXT--
{research_paper}
--END USER PROVIDED TEXT--

Do not respond in full sentences, only create a json object that satisfies the json schema specified in the response format.

Answer:
"""
