# TODO: Cleanup how we are registering these functions as tools...
from datetime import datetime
from openai import OpenAI
from core.entities import Tool
from core.openai.prompts.petrinet_config import PETRINET_PROMPT
from core.openai.prompts.model_card import MODEL_CARD_TEMPLATE, INSTRUCTIONS

### This file contains utility functions for the tool. You can use these functions to solve your task. ###

def escape_curly_braces(text: str):
    """
    Escapes curly braces in a string.
    """
    return text.replace('{', '{{').replace('}', '}}')


def flim_flam(x: int):
    """
    Calculates flim flam from an integer.
    Example Usage: flim_flam(10) -> 50
    """

    return x * (2**2) + 10


def flam_flim(x: int):
    """
    Calculates flam flim from an integer.
    Example Usage: flam_flim(10) -> 12.5
    """
    return x * 2**-2 + 10


def ask_a_human(human_instructions: str):
    """
    Asks the end user for their input. Useful if there are no existing tools to solve your task.
    You can rely on the user to search the web, provide personal details, and generally provide you with up-to-date information.
    Only invoke this function if absolutely necessary, if you can't find a tool to solve your task. Do not bother the human with trivial tasks.
    """
    return input(human_instructions)


def _model_config_chain(research_paper: str, amr: str) -> str:
    print('Reading model config from research paper: {}'.format(research_paper[:100]))
    prompt = PETRINET_PROMPT.format(petrinet=escape_curly_braces(amr), research_paper=escape_curly_braces(research_paper))
    client = OpenAI()
    output = client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=0.0,
        max_tokens=4000,
        messages=[
        {"role": "user", "content": prompt},])

    return "{" + output.choices[0].message.content

def _model_card_chain(research_paper: str):
    print('Reading model card from research paper: {}'.format(research_paper[:100]))
    prompt = INSTRUCTIONS.format(research_paper=escape_curly_braces(research_paper),
                                 model_card_template=MODEL_CARD_TEMPLATE)
    client = OpenAI()
    output = client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=0.0,
        max_tokens=4000,
        messages=[
        {"role": "user", "content": prompt},])
    return "{'ModelName'" + output.choices[0].message.content


# def read_paper_txt_local(path):
#     """
#     Reads text file from local machine.
#     """
#     print('Reading paper from local path: {}'.format(path))
#     paper_text = "-----PAPER START------\n"
#     with open(path, 'r') as file:
#         paper_text += file.read()
#         paper_text += "\n-----PAPER END------"
#     return escape_curly_braces(paper_text)


# def get_model_config(research_paper_path: str):
#     """
#     Accepts path to text of a research paper and returns a petrinet json model configuration if it is possible to parse one from the research paper.
#     The function can handle the entire research paper body and is aware of what is necessary to parse out the final model configuration.
#     """
#     research_paper_text = read_paper_txt_local(research_paper_path)
#     return _model_config_chain(research_paper_text)


# def read_paper_pdf_local(local_absolute_path: str):
#     """
#     Loads a research paper from a path. loads from PDF to plaintext
#     """
#     return convert_pdf_to_text(local_absolute_path)

def get_date(date_format='%Y-%m-%d'):
    """
    Returns the current date.
    """
    return datetime.now().strftime(date_format)

_flam_flim = Tool(name='flam_flim',
                  args=['x'],
                  description='Calculates flam flim from an integer. Example Usage: flam_flim(10) -> 12.5',
                  func=flam_flim,
                  input_type=int)

_flim_flam = Tool(name='flim_flam',
                  args=['x'],
                  description='Calculates flim flam from an integer. Example Usage: flim_flam(10) -> 50',
                  func=flim_flam,
                  input_type=int)

_ask_a_human = Tool(name='ask_a_human',
                    args=['human_instructions'],
                    description='Asks the end user for their input. Useful if there are no existing tools to solve your task. You can rely on the user to search the web, provide personal details, and generally provide you with up-to-date information.',
                    func=ask_a_human,
                    input_type=str)

# _get_model_config = Tool(name='get_model_config',
#                          args=['research_paper_text'],
#                          description='Accepts path to text fil of a research paper, and returns a petrinet json model configuration if it is possible to parse one from the research paper. The function can handle the entire research paper body and is aware of what is necessary to parse out the final model config.',
#                          func=get_model_config,
#                          input_type=str)

# _read_paper_pdf_local = Tool(name='read_paper_pdf_local',
#                              args=['local_absolute_path'],
#                              description='Loads a PDF research paper from a local path on the user\'s PC. loads from PDF to plaintext',
#                              func=read_paper_pdf_local,
#                              input_type=str)
# _read_paper_txt_local = Tool(name='read_paper_txt_local',
#                              args=['local_absolute_path'],
#                              description='Loads a .txt research paper from a local path on the user\'s PC.',
#                              func=read_paper_txt_local,
#                              input_type=str)
