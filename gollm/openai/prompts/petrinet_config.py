PETRINET_PROMPT = """
You are a helpful agent designed to find multiple model configurations for a given Petri net model of various conditions described in a research paper.

Use the following Petri net JSON file as a reference:

---START PETRI NET MODEL JSON---
{petrinet}
---END PETRI NET MODEL JSON---

Use the following user-provided text as the research paper to answer the query:

---START USER-PROVIDED TEXT---
{research_paper}
---END USER-PROVIDED TEXT---

Assume that the user-provided text describes multiple conditions to which the model can be applied. Create a model configuration for each condition.
Be sure to extract parameter values and initial values from the user-provided text, and do not use the default values from the Petri net model.
Be sure to use consistent naming conventions for the conditions. Instead of 'condition_1' and 'condition_2', use descriptive names.

For each condition, create a model configuration JSON object that satisfies the JSON schema specified in the response format. To do this, follow the instructions below:
1.	Create a value for `name` and `description` from the user-provided text.
2.	For the description, provide a long-form description of the condition. If the description cannot be created from the user-provided text, set it to an empty string.
3.	`model_id` should reference the id of the Petri net model.
4.	For each initial specified in the Petri net model ODE semantics, create an initial semantic object. Do not create new initial semantic objects if they are not included in the original Petri net model. You should set initial semantic object fields using the following rules:
    a.	`target` should reference the id of the initial variable from the Petri net model ODE semantics.
    b.	`source` should reference the title or file name of the research paper.
    c.	`type` should be set to "initial”.
    d.	`expression` should be written in LaTeX format.
    e.	`expression_mathml` should be written in MathML format.
    f.	For `expression` and `expression_mathml`, Ensure both are valid and represent the same unit. If the unit is not found or not valid, omit the units field.
5.	For each parameter specified in the Petri net model ODE semantics, create a parameter semantic object. Do not create new parameter semantic objects if they are not included in the original Petri net model. You should set parameter semantic object fields using the following rules:
    a.	`reference_id` should reference the id of the parameter.
    b.	`source` should reference the title or file name of the research paper.
    c.	`type` should be set to "parameter".
    d.	Be sure to extract parameter values from the user-provided text, and do not use the default values from the Petri net model.
        -	If the extracted parameter value is a single constant value, set the parameter `value` to the constant value and set `type` to "Constant".
        -	If the extracted parameter value is a distribution with a maximum and minimum value, set `type` to only "Uniform" and populate the `minimum` and `maximum` fields.

Do not respond in full sentences; only create a JSON object that satisfies the JSON schema specified in the response format.

Answer:
"""
