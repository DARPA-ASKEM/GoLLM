import json
import regex as re
import tiktoken


def remove_references(text: str) -> str:
    """
    Removes reference sections from a scientific paper.
    """
    pattern = r"References\n([\s\S]*?)(?:\n\n|\Z)"
    new_text = re.sub(pattern, "", text)
    return new_text.strip()


def parse_json_from_markdown(text):
    print("Stripping markdown...")
    json_pattern = r"```json\s*(\{.*?\})\s*```"
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        print(f"No markdown found in text: {text}")
        return text


def extract_json(text: str) -> dict:
    corrected_text = text.replace("{{", "{").replace("}}", "}")
    try:
        json_obj = json.loads(corrected_text)
        return json_obj
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}\nfrom text {text}")


def postprocess_oai_json(output: str) -> dict:
    output = "{" + parse_json_from_markdown(
        output
    )  # curly bracket is used in all prompts to denote start of json.
    return extract_json(output)


def normalize_greek_alphabet(text: str) -> str:
    greek_to_english = {
        "α": "alpha",
        "β": "beta",
        "γ": "gamma",
        "δ": "delta",
        "ε": "epsilon",
        "ζ": "zeta",
        "η": "eta",
        "θ": "theta",
        "ι": "iota",
        "κ": "kappa",
        "λ": "lambda",
        "μ": "mu",
        "ν": "nu",
        "ξ": "xi",
        "ο": "omicron",
        "π": "pi",
        "ρ": "rho",
        "σ": "sigma",
        "τ": "tau",
        "υ": "upsilon",
        "φ": "phi",
        "χ": "chi",
        "ψ": "psi",
        "ω": "omega",
    }

    normalized_text = ""
    for char in text:
        if char.lower() in greek_to_english:
            normalized_text += greek_to_english[char.lower()]
        else:
            normalized_text += char
    return normalized_text


def exceeds_tokens(prompt: str, max_tokens: int) -> bool:
    enc = tiktoken.get_encoding("cl100k_base")
    if len(enc.encode(prompt)) > max_tokens:
        return True
    return False


def model_config_adapter(model_config: dict) -> dict:
    """
    Adapter function which converts the model config dict to HMI expected format.
    """

    output_json = {"conditions": []}
    for condition_name, description in model_config["conditions"].items():
        condition_data = {
            "name": condition_name,
            "description": description,
            "parameters": [],
        }
        for param_data in model_config["parameters"]:
            param_value = param_data["value"].get(condition_name)
            condition_data["parameters"].append(
                {"id": param_data["id"], "value": param_value, "name": param_data.get("name"), "description": param_data.get("description"), "units": param_data.get("units"), "distribution": param_data.get("distribution")}
            )
        output_json["conditions"].append(condition_data)
    return output_json
