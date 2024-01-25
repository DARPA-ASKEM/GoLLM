import sys
from core.entities import ModelCardModel
from core.openai.tool_utils import _model_card_chain
from core.taskrunner import TaskRunnerInterface

def cleanup():
    pass

def main():
    try:
        taskrunner = TaskRunnerInterface(description='Model Card CLI')
        taskrunner.on_cancellation(cleanup)

        input_dict = taskrunner.read_input_with_timeout()

        input_model = ModelCardModel(**input_dict)
        response = _model_card_chain(research_paper=input_model.research_paper)

        taskrunner.write_output_with_timeout({"response": response})

    except Exception as e:
        sys.stderr.write(f'Error: {str(e)}\n')
        sys.exit(1)

if __name__ == "__main__":
    main()
