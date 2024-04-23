from setuptools import setup, find_packages

setup(
    name="GoLLM",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai==1.6.1",
        "pandas",
        "pydantic==2.5.3",
        "regex",
        "tiktoken",
    ],
    python_requires=">=3.8",
)
