from core.openai.tool_utils import _get_model_config, _ask_a_human
from core.entities import Toolset, Tool

ASKEMConfigDemo = Toolset([_get_model_config, _ask_a_human])
AskHuman = Toolset([_ask_a_human])
