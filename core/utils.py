import json
import regex as re


def escape_newlines(text: str):
    return text.replace("\n", "\\n")


def remove_references(text: str):
    """
    Removes reference sections from a scientific paper.
    """
    pattern = r"References\n([\s\S]*?)(?:\n\n|\Z)"
    new_text = re.sub(pattern, '', text)
    return new_text.strip()


def extract_json(text: str):
    try:
        matches = re.findall(r'\{.*\}', text, re.DOTALL)

        if matches:
            for match in matches:
                try:
                    json_obj = json.loads(match)
                    return json_obj
                except json.JSONDecodeError:
                    continue
        return None
    except Exception as e:
        print(f"An error occurred while parsing JSON: {e}")
        return None
