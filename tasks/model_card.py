import argparse
import json
import sys
from core.entities import ModelCardModel
from core.openai.tool_utils import _model_card_chain
from core.utils import escape_newlines

def main():
    parser = argparse.ArgumentParser(description='Model Card CLI')
    parser.add_argument('--input', required=True, type=str, help='JSON string with research_paper field')
    args = parser.parse_args()

    try:
        input_dict = json.loads(args.input)
        input_model = ModelCardModel(**input_dict)
        response = escape_newlines(_model_card_chain(research_paper=input_model.research_paper))
        print(json.dumps({"response": response}) + '\n')
    except Exception as e:
        sys.stderr.write(f'Error: {str(e)}\n')
        sys.exit(1)

if __name__ == "__main__":
    main()
