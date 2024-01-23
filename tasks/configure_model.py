import argparse
import json
import sys
from core.entities import ConfigureModel
from core.openai.tool_utils import _model_config_chain
from core.utils import escape_newlines

def main():
    parser = argparse.ArgumentParser(description='Configure Model CLI')
    parser.add_argument('--input', required=True, type=str, help='JSON string with research_paper and amr fields')
    args = parser.parse_args()

    try:
        input_dict = json.loads(args.input)
        input_model = ConfigureModel(**input_dict)
        amr = json.dumps(input_model.amr, separators=(',', ':'))
        response = escape_newlines(_model_config_chain(research_paper=input_model.research_paper, amr=amr))
        print(json.dumps({"response": response + '\n'}))
    except Exception as e:
        sys.stderr.write(f'Error: {str(e)}\n')
        sys.exit(1)

if __name__ == "__main__":
    main()
