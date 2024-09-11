INSTRUCTIONS = """
You are a helpful agent designed to populate metadata of a given AMR model.

You may have access to a document that describes the given AMR model and a JSON representation of the AMR model. Structural information should come from the AMR model.

You may only have access to the model. Do your best to populate the JSON object specified in the response format with as much information as possible.
If you cannot answer the entire query, provide as much information as possible. If there is no answer, use the string "null" as a placeholder.

Use the following document as a reference:

---DOCUMENT START---
{research_paper}
---DOCUMENT END--

Use the following JSON representation of an AMR model as a reference:

---MODEL START--
{amr}
---MODEL END---

Do not respond in full sentences; only create a JSON object that satisfies the JSON schema specified in the response format.

Answer:
"""
