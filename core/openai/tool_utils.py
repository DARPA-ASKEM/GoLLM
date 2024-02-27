from datetime import datetime
import json
from openai import OpenAI, AsyncOpenAI
import os
import pandas as pd
import requests
from typing import List
from core.utils import (
	remove_references,
	extract_json,
	normalize_greek_alphabet,
	exceeds_tokens,
	model_config_adapter,
)
from core.openai.toolsets import DatasetConfig
from core.openai.prompts.dataset_config import DATASET_PROMPT
from core.openai.prompts.petrinet_config import PETRINET_PROMPT
from core.openai.prompts.model_card import MODEL_CARD_TEMPLATE, INSTRUCTIONS
from core.openai.prompts.condense import CONDENSE_PROMPT, format_chunks
from core.openai.react import ReActManager, OpenAIAgent, AgentExecutor


def escape_curly_braces(text: str):
	"""
	Escapes curly braces in a string.
	"""
	return text.replace("{", "{{").replace("}", "}}")


def model_config_chain(research_paper: str, amr: str) -> dict:
	print("Reading model config from research paper: {}".format(research_paper[:100]))
	research_paper = remove_references(research_paper)
	research_paper = normalize_greek_alphabet(research_paper)
	prompt = PETRINET_PROMPT.format(
		petrinet=escape_curly_braces(amr),
		research_paper=escape_curly_braces(research_paper),
	)
	client = OpenAI()
	output = client.chat.completions.create(
		model="gpt-4-0125-preview",
		top_p=0,
		max_tokens=4000,
		messages=[
			{"role": "user", "content": prompt},
		],
	)
	config = extract_json("{" + output.choices[0].message.content)
	return model_config_adapter(config)


def model_card_chain(research_paper: str = None, amr: str = None) -> dict:
	print("Creating model card...")
	assert research_paper or amr, "Either research_paper or amr must be provided."
	if not research_paper:
		research_paper = "NO RESEARCH PAPER PROVIDED"
	if not amr:
		amr = "NO MODEL FILE PROVIDED"
	prompt = INSTRUCTIONS.format(
		research_paper=escape_curly_braces(research_paper),
		amr=escape_curly_braces(amr),
		model_card_template=MODEL_CARD_TEMPLATE,
	)
	client = OpenAI()
	output = client.chat.completions.create(
		model="gpt-4-0125-preview",
		top_p=0,
		max_tokens=4000,
		messages=[
			{"role": "user", "content": prompt},
		],
	)
	model_card = extract_json("{" + output.choices[0].message.content)
	if model_card is None:
		return json.loads(MODEL_CARD_TEMPLATE)
	return model_card


def condense_chain(query: str, chunks: List[str], max_tokens: int = 16385) -> str:
	print("Condensing chunks for query: {}".format(query[:100]))
	prompt = CONDENSE_PROMPT.format(query=query, chunks=format_chunks(chunks))
	if exceeds_tokens(prompt, max_tokens):
		raise ValueError(
			"Prompt exceeds max tokens. Reduce number of chunks by reducing K in KNN search."
		)
	client = OpenAI()
	output = client.chat.completions.create(
		model="gpt-3.5-turbo-0125",
		top_p=0,
		max_tokens=1024,
		messages=[
			{"role": "user", "content": prompt},
		],
	)
	return output.choices[0].message.content


async def amodel_card_chain(research_paper: str):
	"""Async, meant to be run via API for batch jobs run offline."""
	print("Reading model card from research paper: {}".format(research_paper[:100]))
	research_paper = remove_references(research_paper)
	prompt = INSTRUCTIONS.format(
		research_paper=escape_curly_braces(research_paper),
		model_card_template=MODEL_CARD_TEMPLATE,
	)

	client = AsyncOpenAI()
	messages = [{"role": "user", "content": prompt}]
	functions = None
	response = await client.chat.completions.create(
		model="gpt-4-1106-preview",
		messages=messages,
		tools=functions,
		temperature=0.0,
		tool_choice=None,
	)
	model_card = extract_json("{" + response.choices[0].message.content)
	if model_card is None:
		return json.loads(MODEL_CARD_TEMPLATE)
	return model_card

def embedding_chain(text: str) -> List:
	print("Creating embeddings for text: {}".format(text[:100]))
	client = OpenAI()
	output = client.embeddings.create(model="text-embedding-ada-002", input=text)
	return output.data[0].embedding

def config_from_dataset(amr: str, dataset_path: str) -> str:
	agent = OpenAIAgent(DatasetConfig)
	react_manager = ReActManager(agent, executor=AgentExecutor(toolset=DatasetConfig))
	query = DATASET_PROMPT.format(amr=amr, dataset_path=dataset_path)
	return react_manager.run(query)
