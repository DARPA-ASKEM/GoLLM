[![Build and Publish](https://github.com/DARPA-ASKEM/service-template/actions/workflows/publish.yaml/badge.svg?event=push)](https://github.com/DARPA-ASKEM/service-template/actions/workflows/publish.yaml)

# GoLLM

This is a repository which contains endpoints for various Terrarium LLM workflows. 


## Running the API

```shell
docker build -t gollm .
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY gollm
```

## AMR configuration from paper and AMR

Once the API has been started, the ```/configure``` endpoint will consume a JSON with the structure:<br>
```json
{
    "research_paper": "This is a long research paper, perhaps 20 pages worth of text.",
    "amr": {}
}
```

The API will return a model configuration candidate with the structure <br>
```json
{
  "response": {}
}
```

where `response` contains the AMR populated with configuration values.<br>

**Note: This is a WIP, is unoptimized and is currently being used as a test case for integrating LLM features with Terrarium.**

## AMR model card from paper

Once the API has been started, the ```/model_card``` endpoint will consume a JSON with the structure:<br>
   
```json
{
    "research_paper": "string"
}
```
<br>
The API will return a model card in JSON format
<br>

```json
{
  "response": {}
}
```

**Note: This is a WIP**

## Running GoLLM task executables.

Start a fresh venv, then install dependencies and build entrypoints for tasks. 
```shell
pip install -e .
```  

Run tasks like so:

```shell
gollm:model_card --input "{\"research_paper\":\"this is a long research paper, perhaps 20 pages worth of text.\"}"
```

Task output is written to stdout, followed by a terminating newline. 
TODO: write dockerfile for running GoLLM tasks as CLI args. 

## License

[Apache License 2.0](LICENSE)
