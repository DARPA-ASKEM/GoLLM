import sys
from core.entities import ModelCompareModel
from core.openai.tool_utils import compare_models
from core.taskrunner import TaskRunnerInterface


def cleanup():
    pass


def main():
    exitCode = 0
    try:
        taskrunner = TaskRunnerInterface(description="Model Comparison CLI")
        taskrunner.on_cancellation(cleanup)

        input_dict = taskrunner.read_input_with_timeout()

        taskrunner.log("Creating ModelCardModel from input")
        input_model = ModelCompareModel(**input_dict)

        taskrunner.log("Sending request to OpenAI API")
        response = compare_models(model_cards=input_model.model_cards)
        taskrunner.log("Received response from OpenAI API")

        taskrunner.write_output_with_timeout({"response": response})

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.stderr.flush()
        exitCode = 1

    taskrunner.log("Shutting down")
    taskrunner.shutdown()
    sys.exit(exitCode)


if __name__ == "__main__":
    main()
