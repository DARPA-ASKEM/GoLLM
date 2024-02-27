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
    entry_points={
        "console_scripts": [
            "gollm:configure_model=tasks.configure_model:main",
            "gollm:model_card=tasks.model_card:main",
            "gollm:embedding=tasks.embedding:main",
        ],
    },
    python_requires=">=3.8",
)
