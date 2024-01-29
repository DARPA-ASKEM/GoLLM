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

        taskrunner.log("Creating ModelCardModel from input")
        input_model = ModelCardModel(**input_dict)

        taskrunner.log("Sending request to OpenAI API")
        response = _model_card_chain(research_paper=input_model.research_paper)
        taskrunner.log("Received response from OpenAI API")

        taskrunner.write_output_with_timeout({"response": response})

    except Exception as e:
        sys.stderr.write(f'Error: {str(e)}\n')
        sys.stderr.flush()
        sys.exit(1)

if __name__ == "__main__":
    main()
