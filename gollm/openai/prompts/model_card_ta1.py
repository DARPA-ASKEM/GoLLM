INSTRUCTIONS = """
I have a text description and code of a model, and I want to extraction a model card from these materials.
I need to extract some metadata from the code and the textual description of the model.

The metadata to be extracted is as follows:
```txt
{FIELDS}
```

The textual description is as follows:
```txt
{TEXT}
```

The model code is as follows:
```
{CODE}
```

Please help me extract the metadata from the code and the textual description of the model.
Print the result in the following format:
```txt
<field name>: <field value>
<field name>: <field value>
<field name>: <field value>
...
```
Do not hallucinate metadata; only print metadata that can be extracted from the code and the textual description.
If the metadata cannot be extracted, please print "UNKNOWN" instead of the field value.
"""
