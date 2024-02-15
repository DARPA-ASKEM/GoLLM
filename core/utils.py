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

def normalize_greek_alphabet(text: str):
    greek_to_english = {
        'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon',
        'ζ': 'zeta', 'η': 'eta', 'θ': 'theta', 'ι': 'iota', 'κ': 'kappa',
        'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron',
        'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon',
        'φ': 'phi', 'χ': 'chi', 'ψ': 'psi', 'ω': 'omega'
    }

    normalized_text = ""
    for char in text:
        if char.lower() in greek_to_english:
            normalized_text += greek_to_english[char.lower()]
        else:
            normalized_text += char
    return normalized_text
