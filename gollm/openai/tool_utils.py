import json
import os
from openai import OpenAI, AsyncOpenAI
from typing import List
from gollm.utils import (
    exceeds_tokens,
    model_config_adapter,
    normalize_greek_alphabet,
    parse_param_initials,
    postprocess_oai_json,
    remove_references,
    validate_schema
)
from gollm.openai.prompts.amr_enrichment import ENRICH_PROMPT
from gollm.openai.prompts.condense import CONDENSE_PROMPT, format_chunks
from gollm.openai.prompts.dataset_config import DATASET_PROMPT
from gollm.openai.prompts.general_instruction import GENERAL_INSTRUCTION_PROMPT
from gollm.openai.prompts.model_card import MODEL_CARD_TEMPLATE, INSTRUCTIONS
from gollm.openai.prompts.model_meta_compare import MODEL_METADATA_COMPARE_PROMPT
from gollm.openai.prompts.petrinet_config import PETRINET_PROMPT
from gollm.openai.react import OpenAIAgent, AgentExecutor, ReActManager
from gollm.openai.toolsets import DatasetConfig

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def escape_curly_braces(text: str):
    """
    Escapes curly braces in a string.
    """
    return text.replace("{", "{{").replace("}", "}}")


def model_config_chain(research_paper: str, amr: str) -> dict:
    print("Extracting and formatting research paper...")
    research_paper = normalize_greek_alphabet(research_paper)

    print("Uploading and validating model configuration schema...")
    config_path = os.path.join(SCRIPT_DIR, 'prompts', 'configuration.json')
    with open(config_path, 'r') as config_file:
        response_schema = json.load(config_file)
    validate_schema(response_schema)

    print("Building prompt to extract model configurations from a reasearch paper...")
    prompt = PETRINET_PROMPT.format(
        petrinet=escape_curly_braces(amr),
        research_paper=escape_curly_braces(research_paper)
    )

    print("Sending request to OpenAI API...")
    client = OpenAI()
    output = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        seed=416,
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "model_configurations",
                "schema": response_schema
            }
        },
        messages=[
            {"role": "user", "content": prompt},
        ]
    )

    print("Received response from OpenAI API. Formatting response to work with HMI...")
    output_json = json.loads(output.choices[0].message.content)
    return model_config_adapter(output_json)


def amr_enrichment_chain(amr: str, research_paper:str) -> dict:
    amr_param_states = parse_param_initials(amr)
    prompt = ENRICH_PROMPT.format(
		param_initial_dict=amr_param_states,
		paper_text=escape_curly_braces(research_paper)
	)
    client = OpenAI()
    output = client.chat.completions.create(
		model="gpt-4o-2024-05-13",
		max_tokens=4000,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0,
		seed=123,
		temperature=0,
		response_format={"type": "json_object"},
		messages=[
			{"role": "user", "content": prompt},
		],
	)
    return postprocess_oai_json(output.choices[0].message.content)


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
        model="gpt-4o-2024-05-13",
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
		temperature=0,
        seed=123,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    model_card = postprocess_oai_json(output.choices[0].message.content)
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
        model="gpt-4o-2024-05-13",
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
		temperature=0,
        seed=123,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return output.choices[0].message.content

def generate_response(instruction: str) -> str:
    prompt = GENERAL_INSTRUCTION_PROMPT.format(instruction=instruction)
    client = OpenAI()
    output = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
		temperature=0,
        seed=123,
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
        model="gpt-4o-2024-05-13",
        messages=messages,
        tools=functions,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
		temperature=0,
        seed=123,
        max_tokens=1024,
        tool_choice=None,
    )
    model_card = postprocess_oai_json(response.choices[0].message.content)
    if model_card is None:
        return json.loads(MODEL_CARD_TEMPLATE)
    return model_card


def embedding_chain(text: str) -> List:
    print("Creating embeddings for text: {}".format(text[:100]))
    client = OpenAI()
    output = client.embeddings.create(model="text-embedding-ada-002", input=text)
    return output.data[0].embedding


def react_config_from_dataset(amr: str, dataset_path: str) -> str:
    agent = OpenAIAgent(DatasetConfig)
    react_manager = ReActManager(agent, executor=AgentExecutor(toolset=DatasetConfig))
    query = DATASET_PROMPT.format(amr=amr, dataset_path=dataset_path)
    return react_manager.run(query)


def config_from_dataset(amr: str, model_mapping: str, datasets: List[str]) -> str:
    dataset_text = ""
    for idx in range(len(datasets)):
        dataset_text += f"..dataset_{idx + 1} start..\n {datasets[idx]} \n...dataset_{idx + 1} end...\n"

    prompt = DATASET_PROMPT.format(amr=amr, matrix_str=model_mapping, datasets=dataset_text)
    client = OpenAI()
    output = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
		temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        seed=123,
        max_tokens=4000,
		response_format={"type": "json_object"},
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return postprocess_oai_json(output.choices[0].message.content)


def compare_models(amrs: List[str]) -> str:
    print("Comparing models...")

    joined_escaped_amrs = "\n------\n".join([escape_curly_braces(amr) for amr in amrs])
    prompt = MODEL_METADATA_COMPARE_PROMPT.format(
        amrs=joined_escaped_amrs
    )

    client = OpenAI()
    output = client.chat.completions.create(
        model="gpt-4o-mini",
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        seed=123,
		temperature=0,
        max_tokens=2048,
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    return output.choices[0].message.content
