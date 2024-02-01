from datetime import datetime
import inspect
from pydantic import BaseModel, root_validator
from typing import List, Callable, Type, Dict


class ConfigureModel(BaseModel):
    research_paper: str
    amr: Dict # expects AMR in JSON format

class ModelCardModel(BaseModel):
    research_paper: str


class EmbeddingModel(BaseModel):
    text: str
    embedding_model: str

    @root_validator(pre=False, skip_on_failure=True)
    def check_embedding_model(cls, values):
        embedding_model = values.get('embedding_model')
        if embedding_model != 'text-embedding-ada-002':
            raise ValueError('Invalid embedding model, must be "text-embedding-ada-002"')
        return values

class Message(BaseModel):
    message_type: str
    message_content: str
    message_id: int = None
    timestamp: datetime = None


    @root_validator(pre=True)
    def set_timestamp_id(cls, values):
        timestamp = values.get('timestamp')
        if timestamp:
            values['timestamp'] = datetime.fromtimestamp(timestamp)
        else:
            values['timestamp'] = datetime.now()
        return values

    @root_validator(pre=True)
    def set_message_id(cls, values):
        timestamp = values.get('timestamp')
        if timestamp:
            values['message_id'] = int(timestamp.timestamp())
        return values


class Action(BaseModel):
    message_id: int
    action_blob: dict


class ChatSession:
    # create session_id from datetime now
    session_id = int(datetime.now().timestamp())

    def __init__(self, system_context: str):
        self.system_context = system_context
        self.conversation_history = []

    def add_message(self, message: Message):
        """
        Add a message to the conversation history.
        """
        self.conversation_history.append(message)

    def get_history(self):
        """
        Get the conversation history.
        :return: List of tuples containing message type and content
        """
        return self.conversation_history


class Tool:
    def __init__(self, name: str, args: List, description: str, func: Callable, input_type: Type):
        self.name = name
        self.args = args
        self.description = description
        self.func = func
        self.input_type = input_type

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class Toolset:
    """
    A class for testing the toolset.
    """
    TOOLS = {}

    def __init__(self, tools: List[Tool]):
        self.TOOLS = {tool.name: tool for tool in tools}

    def get_tool_names(self):
        """
        Returns a string of tool names.
        """
        return '\n'.join(self.TOOLS.keys())

    def get_tool_code(self):
        """
        Returns a string of tool arguments. Used for zero shot ReAct
        """
        return '\n'.join([inspect.getsource(tool.func) for tool in self.TOOLS.values()])

    def get_tool(self, tool_name: str):
        return self.TOOLS[tool_name]

    def run_tool(self, tool_name: str, tool_args):
        """
        Runs a tool.
        """
        tool = self.TOOLS[tool_name]
        return tool(tool.input_type(tool_args))

    def add_tool(self, tool: Tool):
        """
        Adds a tool to the toolset.
        """
        self.TOOLS[tool.name] = tool
