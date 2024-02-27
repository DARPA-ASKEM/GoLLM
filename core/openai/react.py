import json
from openai import OpenAI
import regex as re
from typing import List

from core.openai.prompts.react import (
    SYSTEM_MESSAGE_PREFIX,
    FORMAT_INSTRUCTIONS,
    SYSTEM_MESSAGE_SUFFIX,
    HUMAN_MESSAGE,
)

from core.entities import Message


class OpenAIAgent:
    def __init__(self, toolset, api_key=None, conversation_history=None):
        self.model = OpenAI(api_key=api_key)

        self.toolset = toolset
        self.conversation_history = conversation_history

    def _construct_prompt(self, human_message: str, scratchpad: str = None):
        system_prompt = SYSTEM_MESSAGE_PREFIX + "\n\n"
        system_prompt += self.toolset.get_tool_names() + "\n\n"
        system_prompt += (
            FORMAT_INSTRUCTIONS.format(tool_names=self.toolset.get_tool_code()) + "\n\n"
        )
        system_prompt += SYSTEM_MESSAGE_SUFFIX + "\n\n"
        if scratchpad is None:
            scratchpad = "Thought:"
        human_prompt = HUMAN_MESSAGE.format(input=human_message, scratchpad=scratchpad)
        return (
            system_prompt,
            human_prompt,
        )

    def run(self, human_message: str, scratchpad: str = None):
        sys_prompt, human_prompt = self._construct_prompt(
            human_message, scratchpad=scratchpad
        )
        output = self.model.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=0.0,
            top_p=0,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": human_prompt},
            ],
        )
        output = Message(
            message_content=output.choices[0].message.content, message_type="assistant"
        )
        return output, sys_prompt, human_prompt

class ScratchpadParser:
    thought_pattern = r"Thought:(.*?)(?=Action:|Observation:|$)"
    action_pattern = r"Action:\n```\n({.*?})\n```\n"
    observation_pattern = r"Observation:(.*?)(?=Thought:|Action:|$)"
    action_blob_pattern = r"\{\{\s*'action':\s*(.*?),\s*'action_input':\s*(.*?)\s*\}\}"
    final_answer_pattern = r".*Final Answer: (.*)"

    @staticmethod
    def _strip_newlines(matches: List[str]):
        return [i.replace("\n", "") for i in matches]

    @classmethod
    def get_final_answer(cls, scratchpad: str):
        match = re.search(cls.final_answer_pattern, scratchpad, flags=re.DOTALL)
        if match:
            return match.group(1)
        else:
            raise ValueError(
                f"No final answer found in scratchpad.\nSCRATCHPAD:\n{scratchpad}"
            )

    @classmethod
    def get_actions(cls, scratchpad: str):
        return re.findall(cls.action_pattern, scratchpad, flags=re.DOTALL)

    @classmethod
    def get_observations(cls, scratchpad: str):
        return cls._strip_newlines(
            re.findall(cls.observation_pattern, scratchpad, flags=re.DOTALL)
        )

    @classmethod
    def get_thoughts(cls, scratchpad: str):
        return cls._strip_newlines(
            re.findall(cls.thought_pattern, scratchpad, flags=re.DOTALL)
        )

    @classmethod
    def _match_action_blob(cls, action: str):
        return re.search(cls.action_blob_pattern, action, flags=re.DOTALL).group()


class AgentExecutor:
    def __init__(self, toolset):
        self.toolset = toolset

    def execute(self, agent_action: dict):
        tool_name = agent_action["action"]
        tool_arg = agent_action["action_input"]
        print(f"Executing first found action in scratchpad: {tool_name}")
        tool_output = self.toolset.run_tool(tool_name, tool_arg)
        return {
            "tool_name": tool_name,
            "tool_output": tool_output,
            "tool_input": tool_arg,
        }


class ReActManager:
    def __init__(self, agent, executor, max_errors=5):
        self.agent = agent
        self.executor = executor
        self.scratchpad = "Thought:"
        self.executed_actions = []
        self.n = 0
        self.max_errors = max_errors
        self.errors = 0

    def run(self, query: str):
        while True:
            agent_message, _, _ = self.agent.run(
                human_message=query, scratchpad=self.scratchpad
            )
            agent_output = agent_message.message_content
            ## get actions from agent output..
            actions = ScratchpadParser.get_actions(
                agent_output
            )  # TODO: ensure that all actions are indeed JSON blobs.

            if actions is None:
                self._increment_error(
                    f"Error encountered when parsing agent output, no actions found: {agent_output}"
                )

            # Assumption: We should not execute the exact same action twice within the react loop.
            pending_actions = [
                action for action in actions if action not in self.executed_actions
            ]

            if "Final Answer:" in agent_output and len(pending_actions) == 0:
                self.scratchpad += agent_output
                break

            # Execute only one action at a time.
            self.scratchpad += agent_output

            try:
                first_pending_action_index = self.scratchpad.index(pending_actions[0])
            except IndexError:
                self._increment_error(
                    f"No pending actions found in agent output: {agent_output}"
                )
                continue

            ### log extraneous generated text ###
            print(
                f"Extraneous Text Truncated: {self.scratchpad[first_pending_action_index + len(pending_actions[0]):]}"
            )

            self.scratchpad = self.scratchpad[
                : first_pending_action_index + len(pending_actions[0])
            ]

            try:
                action_blob = json.loads(pending_actions[0])
            except json.decoder.JSONDecodeError:
                self._increment_error(
                    f"Invalid json blob in agent output: {pending_actions[0]}"
                )
                self.scratchpad.replace(pending_actions[0], "")
                continue

            executor_blob = self.executor.execute(action_blob)
            self.executed_actions.append(pending_actions[0])
            observation = executor_blob["tool_output"]
            self.scratchpad += f"Observation:{observation}\n"
            self.n += 1
            self._log(f"Iteration {self.n}")
            if self.n > 5:
                break
        self._log(self.scratchpad)
        return self.scratchpad

    def _increment_error(self, msg: str):
        self.errors += 1
        self._log(msg)
        if self.errors > self.max_errors:
            raise ValueError("Too many errors, exiting.")

    def _log(self, message):
        print(message)
