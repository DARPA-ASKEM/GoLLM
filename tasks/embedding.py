import sys
from core.entities import EmbeddingModel
from core.openai.tool_utils import embedding_chain
from core.taskrunner import TaskRunnerInterface


def cleanup():
    pass


def main():
    try:
        taskrunner = TaskRunnerInterface(description="Embedding CLI")
        taskrunner.on_cancellation(cleanup)

        input_dict = taskrunner.read_input_with_timeout()

        taskrunner.log("Creating Embedding from input")
        input_model = EmbeddingModel(**input_dict)

        taskrunner.log("Sending request to OpenAI API")
        response = embedding_chain(text=input_model.text)
        taskrunner.log("Received response from OpenAI API")

        taskrunner.write_output_with_timeout({"response": response})

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.stderr.flush()
        sys.exit(1)


if __name__ == "__main__":
    main()
