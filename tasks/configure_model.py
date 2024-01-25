import argparse
import json
import sys
from core.entities import ConfigureModel
from core.openai.tool_utils import _model_config_chain
from core.taskrunner import TaskRunnerInterface

def cleanup():
    pass

def main():
    try:
        taskrunner = TaskRunnerInterface(description='Configure Model CLI')
        taskrunner.on_cancellation(cleanup)

        input_dict = taskrunner.read_input_with_timeout()

        input_model = ConfigureModel(**input_dict)
        amr = json.dumps(input_model.amr, separators=(',', ':'))
        response = _model_config_chain(research_paper=input_model.research_paper, amr=amr)

        taskrunner.write_output_with_timeout({"response": response})

    except Exception as e:
        sys.stderr.write(f'Error: {str(e)}\n')
        sys.exit(1)

if __name__ == "__main__":
    main()
