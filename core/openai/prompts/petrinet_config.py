PETRINET_PROMPT = """
      You are a helpful chatbot designed to find initial parameters for a given petri net model file and a given research paper describing the mathematical model.
      Use the following petri net json file as a reference: {petrinet}.
      Assume that parameter fields with missing values may have multiple different sets values discussed in the research paper for different conditions.\n
      Return the different sets of initial parameters for the petri net model file like so:
	  "parameters": [{{
      "id": "beta",
      "value": {{'condition_1': 0.1, 'condition_2': 0.2}},
      ....
      }}
	  ],
      If a condition is not mentioned in the research paper, then the value should be set to null. Be sure to use consistent naming conventions for the conditions. Instead of 'condition_1' and 'condition_2'.. use names that are descriptive of the conditions.
      Only use parameters found in the reference petrinet file provided above.
      Ensure that the output follows the above petri net format and can be serialized as a JSON. Specifically populate parameters and initials. Use the following
      research paper to answer the user's query: {research_paper}\n\n Answer:
      ```json
         {{
"""
