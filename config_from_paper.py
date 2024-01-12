import argparse
import json
from core.openai.react import OpenAIAgent, AgentExecutor, ReActManager
from core.openai.tool_utils import _model_config_chain


def main():

    # this CLI expects a JSON with the following format:
    # {
    #     "research_paper": str,
    #     "amr": str,
    # }
    # assume this will be run through docker and we want to return the response as a JSON

    parser = argparse.ArgumentParser(description='Uncharted LLM Demo')
    parser.add_argument('--input', type=str, help='JSON input path')
    args = parser.parse_args()
    with open(args.input, 'r') as f:
        input_json = json.loads(f.read())
    ## ensure that keys are correct, TODO: add holistic validation. These lazy tests are just for hello world.
    assert 'research_paper' in input_json.keys()
    assert 'amr' in input_json.keys()
    amr = json.dumps(input_json['amr'], separators=(',', ':'))
    research_paper = input_json['research_paper']
    response = _model_config_chain(research_paper=research_paper, amr=amr)
    print(json.dumps(response))

if __name__ == '__main__':
    main()
