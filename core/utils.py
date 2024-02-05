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
