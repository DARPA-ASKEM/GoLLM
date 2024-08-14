from setuptools import setup, find_packages

setup(
    name="GoLLM",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai==1.40.6",
        "pandas",
        "pydantic==2.8.2",
        "regex",
        "tiktoken",
    ],
	package_data={"gollm.openai.prompts": ["*.json"]},
	include_package_data=True,
    python_requires=">=3.11",
)
