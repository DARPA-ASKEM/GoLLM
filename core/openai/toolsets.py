from core.openai.tool_utils import read_csv, get_date, ask_a_human, download_from_presigned_url
from core.entities import Toolset, Tool



with Toolset() as DatasetConfig:
    DatasetConfig.add_tool(
        "ask_a_human",
        ["human_instructions"],
        "Asks the end user for their input. Useful if there are no existing tools to solve your task. You can rely on the user to search the web, provide personal details, and generally provide you with up-to-date information.",
        ask_a_human,
        str,
    )
    DatasetConfig.add_tool(
		"get_date",
		["date_format"],
		"Returns the current date.",
		get_date,
		str,
	)
    DatasetConfig.add_tool(
		"read_csv",
		["file_path", "**kwargs"],
		"Reads a CSV file into a pandas DataFrame.",
		read_csv,
		str,
	)
    DatasetConfig.add_tool(
		"download_from_presigned_url",
		["presigned_url"],
		"Download file from a presigned URL and save it in the working directory with the same name.",
		download_from_presigned_url,
		str,
	)
