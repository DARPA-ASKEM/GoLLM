[![Build and Publish](https://github.com/DARPA-ASKEM/service-template/actions/workflows/publish.yaml/badge.svg?event=push)](https://github.com/DARPA-ASKEM/service-template/actions/workflows/publish.yaml)

# GoLLM

This is a repository which contains endpoints for various Terrarium LLM workflows.

# Getting Started

## Running the API

`cd` into root<br>
run: ```docker build -t gollm .```<br>
run: ```docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY gollm```

## AMR configuration from paper and AMR

Once the API has been started, the ```/configure``` endpoint will consume a JSON with the structure:<br>
    ```
    {
    research_paper: str,
    amr: obj
    }
    ```<br>

The API will return a model configuration candidate with the structure <br>
```
{response: obj}
```
<br>
where `response` contains the AMR populated with configuration values.<br>

<b>Note: This is a WIP, is unoptimized and is currently being used as a test case for integrating LLM features with Terrarium. </b>

## AMR model card from paper

Once the API has been started, the ```/model_card``` endpoint will consume a JSON with the structure:<br>

```
    {
    research_paper: str,
    }
```
<br>
The API will return a model card in JSON format
<br>

```
{response: obj}
```

<b> Note: This is a WIP </b>

<hr>

## License

[Apache License 2.0](LICENSE)
