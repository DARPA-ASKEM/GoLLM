import json
import sys
from core.entities import ConfigureModel
from core.openai.tool_utils import model_config_chain
from core.taskrunner import TaskRunnerInterface


def cleanup():
    pass


def main():
    try:
        taskrunner = TaskRunnerInterface(description="Configure Model CLI")
        taskrunner.on_cancellation(cleanup)

        input_dict = taskrunner.read_input_with_timeout()

        taskrunner.log("Creating ConfigureModel from input")
        input_model = ConfigureModel(**input_dict)
        amr = json.dumps(input_model.amr, separators=(",", ":"))

        taskrunner.log("Sending request to OpenAI API")
        response = model_config_chain(
            research_paper=input_model.research_paper, amr=amr
        )
        taskrunner.log("Received response from OpenAI API")

        taskrunner.write_output_with_timeout({"response": response})

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.stderr.flush()
        sys.exit(1)


if __name__ == "__main__":
    main()
