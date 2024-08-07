import json
import os
from openai import OpenAI, AsyncOpenAI
from typing import List
from gollm.utils import (
    remove_references,
    normalize_greek_alphabet,
    exceeds_tokens,
    model_config_adapter,
    postprocess_oai_json,
)
from gollm.openai.prompts.petrinet_config import PETRINET_PROMPT
from gollm.openai.prompts.model_card import MODEL_CARD_TEMPLATE, INSTRUCTIONS
from gollm.openai.prompts.condense import CONDENSE_PROMPT, format_chunks
from gollm.openai.prompts.dataset_config import DATASET_PROMPT
from gollm.openai.prompts.model_meta_compare import MODEL_METADATA_COMPARE_PROMPT
from gollm.openai.prompts.general_instruction import GENERAL_INSTRUCTION_PROMPT
from gollm.openai.react import OpenAIAgent, AgentExecutor, ReActManager
from gollm.openai.toolsets import DatasetConfig

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def escape_curly_braces(text: str):
    """
    Escapes curly braces in a string.
    """
    return text.replace("{", "{{").replace("}", "}}")


def model_config_chain(research_paper: str, amr: str) -> dict:
    print("Reading model config from research paper: {}".format(research_paper[:100]))
    research_paper = remove_references(research_paper)
    research_paper = normalize_greek_alphabet(research_paper)

	# probonto ontology file copied from https://github.com/gyorilab/mira/blob/e468059089681c7cd457acc51821b5bd1074df04/mira/dkg/resources/probonto.json
    json_path = os.path.join(SCRIPT_DIR, 'prompts', 'probonto.json')
    with open(json_path, 'r') as f:
        pb = json.load(f)

    prompt = PETRINET_PROMPT.format(
        petrinet=escape_curly_braces(amr),
        research_paper=escape_curly_braces(research_paper),
		pb=escape_curly_braces(json.dumps(pb))
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
    config = postprocess_oai_json(output.choices[0].message.content)
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


def compare_models(model_cards: List[str]) -> str:
    prompt = MODEL_METADATA_COMPARE_PROMPT.format(
        model_cards="--------".join(model_cards)
    )
    client = OpenAI()
    output = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        seed=123,
		temperature=0,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return output.choices[0].message.content
