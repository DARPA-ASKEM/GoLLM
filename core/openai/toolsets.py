import pandas as pd
import requests
from datetime import datetime
import os
from core.entities import Toolset


### Tools for ReACt ###


def ask_a_human(action_input: str):
	"""
	Asks the end user for their input. Useful if there are no existing tools to solve your task.
	You can rely on the user to search the web, provide personal details, and generally provide you with up-to-date information.
	Only invoke this function if absolutely necessary, if you can't find a tool to solve your task. Do not bother the human with trivial tasks.
	"""
	return input(action_input)


def get_date(action_input="%Y-%m-%d"):
	"""
	Returns the current date.
	"""
	return datetime.now().strftime(action_input)


def read_csv(action_input: str, **kwargs) -> pd.DataFrame:
	"""
	Reads a CSV file into a pandas DataFrame.
	"""
	return pd.read_csv(action_input, **kwargs)


def download_from_presigned_url(presigned_url: str):
	"""
	Download file from a presigned URL and save it in the working directory with the same name.

	Args:
		presigned_url (str): The presigned URL for the file.
	"""
	# Extract filename from the presigned URL
	filename = presigned_url.split('/')[-1]

	# Check if the file is already cached
	if os.path.exists(filename):
		print("File already cached.")
		return

	try:
		# Download the file from the presigned URL
		print("Downloading from presigned URL...")
		response = requests.get(presigned_url)
		with open(filename, 'wb') as f:
			f.write(response.content)
		print("Download complete.")
	except Exception as e:
		print(f"Error downloading file from presigned URL: {e}")

### Toolsets ###

with Toolset() as DatasetConfig:

    DatasetConfig.add_tool(
		"read_csv",
		["file_path", "**kwargs"],
		"Reads a CSV file into a pandas DataFrame. This gives you access to the user\'s local machine",
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
