# This is not to be used for production yet.
REACT_DATASET_PROMPT = """
	You are a helpful agent that will accept a representation of a mathematical model and a dataset which contains parameter values which must be mapped into the mathematical model. You have access to tools which can help you fetch and manipulate datasets.
	The mathematical models may be represented in petri nets, regnets, stockflow models, or other model formats. The dataset may be in the form of a matrix where the index and column names are useful for mapping the initials, values, or parameters, within the dataset to the model.
	Your goal is to map the dataset to the model and provide the results of the mapping. If you cannot map the dataset to the model, use the string "null" as a placeholder.
	Use the following model configuration as a reference: ---MODEL CONFIGURATION START---{amr}---MODEL CONFIGURATION END---. --PATH TO DATASET START---{dataset_path}---PATH TO DATASET END--. Ensure that the output follows the below model configuration and is JSON serializable.
	Once you have enough information from loading the dataset in your scratchpad, populate the missing values in the configuration as your final answer. Only write the parameter section of the configuration, not the entire configuration. Pay close attention to which parameter corresponds to which linkage:
	{{

"""

DATASET_PROMPT = """
	You are a helpful agent that will accept a representation of a mathematical model and one or more dataset which contain parameter and initials values which must be mapped into the mathematical model.
	The mathematical models may be represented in petri nets, regnets, stockflow models, or other model formats. You may need to use parameter mappings, in the form of matrices, to map between initials, transitions and parameters. Pay attention to the dataset row and column names as well as the model mappings.

	---EXAMPLE---


	---MODEL MAPPING START ---

	...
	subject-controllers of f

	,S_1,S_2,S_3
	I_1,f_0,f_1,f_2
	I_2,f_4,f_3,f_5
	I_3,f_7,f_8,f_6

	...

	---MODEL MAPPING END ---

	--DATASETS START--
	age group,I_1,I_2,I_3
	S_1,38.620784763504,20.5607763176635,6.11741392364261
	S_2,20.5607763176635,28.2162969616496,11.5991952643675
	S_3,6.11741392364261,11.5991952643675,20.013468013468

	--DATASETS END--

	Since the subject controller of f_0 is I_1, S_1, we want to map the value from the dataset cell S_1, I_1 to f_0..

	values: [
			{{"id": "f_0", "value": 38.620784763504}},
			...
			]

	Based on this information, we do not know what the initial values for I_1 and S_1 are. Do not misinterpret these kinds of interaction values as initials.

	Only populate values from the datasets. If a value is not present in the datasets, use the default value from the model configuration, or null.
	The datasets may be in the form of a matrix where the index and column names are useful for mapping the values of initials and parameters within the dataset to the model.
	Your goal is to map the dataset to the model and provide the results of the mapping. If you cannot map the dataset to the model, use the string "null" as a placeholder.
	Use the following model configuration as a reference: ---MODEL CONFIGURATION START---{amr}---MODEL CONFIGURATION END---.  ---DATASETS START---{datasets}---DATASETS END--. Ensure that the output follows the below model configuration and is JSON serializable.
	Once you have enough information from loading the dataset in your scratchpad, populate the missing values in the configuration as your final answer. Parameters should follow the format:\n
		values: [
			{{"id": "str", "value": float, "type": "parameter" or "initial"}},
			...
			]
	Only write the ids and values of initials and parameters, do not write the entire configuration. Pay close attention to which parameter corresponds to which linkage. Do not generate markdown and ensure your output is JSON serializable:
	OUTPUT: {{
"""
