PETRINET_PROMPT = """
      You are a helpful agent designed to find initial parameters for a given petri net model file and a given research paper describing the mathematical model.
      Use the following petri net json file as a reference: {petrinet}.
	  Do not respond in full sentences, only populate the JSON output with conditions and parameters.

      Assume that parameter fields with missing values may have multiple different sets values discussed in the user provided text for different conditions.\n
      Return the different sets of initial parameters for the petri net model file like so:
	  {{"conditions": {{"condition_1": "description of condition_1", "condition_2": "description of condition_2", ...}},
	  "parameters": [{{
      "id": "beta",
      "value": {{'condition_1': 0.1, 'condition_2': 0.2}},
	  "description": "Description of the parameter beta",
	  "units": {{ "expression": "1.0e-9*mole/liter", "expression_mathml": "<apply><divide/><apply><times/><cn>1.0000000000000001e-9</cn><ci>mole</ci></apply><ci>liter</ci></apply>" }}
      ....
      }}
	  ],
      }}
      If a condition is not mentioned in the following text body, then the value should be set to the string "null". Be sure to use consistent naming conventions for the conditions.
      Instead of 'condition_1' and 'condition_2'.. use names that are descriptive of the conditions.

      Populate the description, and the units fields for each parameter. If the description can not be found, use the parameter's name if available, otherwise set it to "null".
	  For units, provide both "units.expression" (a unicode string) and "units.expression_mathml" (MathML format). If the unit is not provided or invalid, omit the units field.

  	  Only use parameters found in the reference petrinet file provided above.
      Ensure that the output follows the above petri net format and can be serialized as a JSON. Specifically populate parameters and initials. Use the following
      text body to answer the user's query: --START USER PROVIDED TEXT-- {research_paper}--END USER PROVIDED TEXT--\n\n Answer:
         {{
"""
	#   For units, provide both "units.expression" (a unicode string) and "units.expression_mathml" (MathML format). If the unit is not provided or invalid, set the 'units' field to "null".


#       If a condition is not mentioned in the following text body, then the value should be set to the string "null". Be sure to use consistent naming conventions for the conditions.
#       Instead of 'condition_1' and 'condition_2'.. use names that are descriptive of the conditions.

#       Populate the description, and the units fields for each parameter. If the description can not be found, use the parameter's name if available, otherwise set it to "null".
#       For units, provide both "units.expression" with a unicode string representing the expression and "units.expression_mathml" with the MathML representation of the expression. If the unit expression is not extracted from the text body, not a valid unit, then the value of the 'units' field should be set to "null".

#   	  Only use parameters found in the reference petrinet file provided above.
#       Ensure that the output follows the above petri net format and can be serialized as a JSON. Specifically populate parameters and initials. Use the following
#       text body to answer the user's query: --START USER PROVIDED TEXT-- {research_paper}--END USER PROVIDED TEXT--\n\n Answer:
#          {{
# """
