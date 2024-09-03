CONFIGURE_FROM_PAPER_PROMPT = """
You are a helpful agent designed to find multiple model configurations for a given AMR model of various conditions described in a research paper.

Use the following AMR model JSON file as a reference:

---START AMR MODEL JSON---
{amr}
---END AMR MODEL JSON---

Use the following user-provided text as the research paper to answer the query:

---START USER-PROVIDED TEXT---
{research_paper}
---END USER-PROVIDED TEXT---

Assume that the user-provided text describes multiple conditions to which the model can be applied. Create a model configuration for each condition.
Be sure to extract parameter values and initial values from the user-provided text, and do not use the default values from the AMR model.
Be sure to use consistent naming conventions for the conditions. Instead of 'condition_1' and 'condition_2', use descriptive names.

For each condition, create a model configuration JSON object that satisfies the JSON schema specified in the response format. To do this, follow the instructions below:
1.	Create a value for `name` and `description` from the user-provided text.
2.	For the description, provide a long-form description of the condition. If the description cannot be created from the user-provided text, set it to an empty string.
3.	`model_id` id a UUID. If the AMR model has an id, you can use it. Otherwise, you can set as the nil UUID "00000000-0000-0000-0000-000000000000".
4.	For each initial specified in the AMR model ODE semantics, create an initial semantic object. Do not create new initial semantic objects if they are not included in the original AMR model. You should set initial semantic object fields using the following rules:
    a.	`target` should reference the id of the initial variable from the AMR model ODE semantics.
    b.	`source` should reference the title or file name of the research paper.
    c.	`type` should be set to "initial”.
    d.	You should extract a numerical value or an expression of the initial state from the user-provided text if possible and add it to `expression`
    e.	`expression_mathml` should be `expression` written in MathML format.
5.	For each parameter specified in the AMR model ODE semantics, create a parameter semantic object. Do not create new parameter semantic objects if they are not included in the original AMR model. You should set parameter semantic object fields using the following rules:
    a.	`reference_id` should reference the id of the parameter.
    b.	`source` should reference the title or file name of the research paper.
    c.	`type` should be set to "parameter".
    d.	Be sure to extract parameter values from the user-provided text, and do not use the default values from the AMR model.
        -	If the extracted parameter value is a single constant value, set the parameter `value` to the constant value and set `type` to "Constant".
        -	If the extracted parameter value is a distribution with a maximum and minimum value, set `type` to only "Uniform" and populate the `minimum` and `maximum` fields.

Do not respond in full sentences; only create a JSON object that satisfies the JSON schema specified in the response format.

Answer:
"""
