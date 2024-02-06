from datetime import datetime
import json
from openai import OpenAI, AsyncOpenAI
from typing import List
from core.entities import Tool
from core.utils import remove_references, extract_json
from core.openai.prompts.petrinet_config import PETRINET_PROMPT
from core.openai.prompts.model_card import MODEL_CARD_TEMPLATE, INSTRUCTIONS


def escape_curly_braces(text: str):
    """
    Escapes curly braces in a string.
    """
    return text.replace("{", "{{").replace("}", "}}")


def ask_a_human(human_instructions: str):
    """
    Asks the end user for their input. Useful if there are no existing tools to solve your task.
    You can rely on the user to search the web, provide personal details, and generally provide you with up-to-date information.
    Only invoke this function if absolutely necessary, if you can't find a tool to solve your task. Do not bother the human with trivial tasks.
    """
    return input(human_instructions)


def model_config_chain(research_paper: str, amr: str) -> str:
    print("Reading model config from research paper: {}".format(research_paper[:100]))
    research_paper = remove_references(research_paper)
    prompt = PETRINET_PROMPT.format(
        petrinet=escape_curly_braces(amr),
        research_paper=escape_curly_braces(research_paper),
    )
    client = OpenAI()
    output = client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=0.0,
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return "{" + output.choices[0].message.content


def model_card_chain(research_paper: str):
    print("Reading model card from research paper: {}".format(research_paper[:100]))
    prompt = INSTRUCTIONS.format(
        research_paper=escape_curly_braces(research_paper),
        model_card_template=MODEL_CARD_TEMPLATE,
    )
    client = OpenAI()
    output = client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=0.0,
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    model_card = extract_json("{" + output.choices[0].message.content)
    if model_card is None:
        return json.loads(MODEL_CARD_TEMPLATE)
    return model_card


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
        tool_choice=None
    )
    model_card = extract_json("{" + response.choices[0].message.content)
    if model_card is None:
        return json.loads(MODEL_CARD_TEMPLATE)
    return model_card


def embedding_chain(text: str) -> List:
    print("Creating embeddings for text: {}".format(text[:100]))
    client = OpenAI()
    output = client.embeddings.create(model="text-embedding-ada-002", input=text)
    print(type(output.data[0].embedding))
    return output.data[0].embedding


def get_date(date_format="%Y-%m-%d"):
    """
    Returns the current date.
    """
    return datetime.now().strftime(date_format)


_ask_a_human = Tool(
    name="ask_a_human",
    args=["human_instructions"],
    description="Asks the end user for their input. Useful if there are no existing tools to solve your task. You can rely on the user to search the web, provide personal details, and generally provide you with up-to-date information.",
    func=ask_a_human,
    input_type=str,
)
