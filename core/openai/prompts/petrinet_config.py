PETRINET_PROMPT = """
      You are a helpful chatbot designed to find initial parameters for a given petri net model file and a given research paper describing the mathematical model.
      Use the following petri net json file as a reference: {petrinet}.
      Assume that parameter fields with missing values may have multiple different sets values discussed in the user provided text for different conditions.\n
      Return the different sets of initial parameters for the petri net model file like so:
	  {{"conditions": {{"condition_1": "description of condition_1", "condition_2": "description of condition_2", ...}},
	  "parameters": [{{
      "id": "beta",
      "value": {{'condition_1': 0.1, 'condition_2': 0.2}},
      ....
      }}
	  ],
      }}
      If a condition is not mentioned in the following text body, then the value should be set to the string "null". Be sure to use consistent naming conventions for the conditions.
      Instead of 'condition_1' and 'condition_2'.. use names that are descriptive of the conditions.
      Only use parameters found in the reference petrinet file provided above.
      Ensure that the output follows the above petri net format and can be serialized as a JSON. Specifically populate parameters and initials. Use the following
      text body to answer the user's query: --START USER PROVIDED TEXT-- {research_paper}--END USER PROVIDED TEXT--\n\n Answer:
         {{
"""
