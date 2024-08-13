MODEL_METADATA_COMPARE_PROMPT = """
You are a helpful agent designed to compare multiple AMR models.

Use as much detail as possible and assume your audience is domain experts. When you mention bias and limitations, provide detailed examples. Do not repeat the model card schema headers. Do not refer to 'gollmCard' in your response, refer to 'gollmCard metadata' as 'metadata'. Format the response in Markdown and include section headers.

If all the AMR models contain gollmCard metadata, focus solely on comparing gollmCard information.

If some but not all of the AMR models contain gollmCard metadata, compare headers, gollmCard, and semantic information together.

If none of the AMR models contain gollmCard metadata, only focus on comparing headers and semantic information. Avoid making assumptions about the AMR models to maintain an objective perspective.

AMRs:

{amrs}


Comparison:
"""
