import unittest
from gollm.openai.react import AgentExecutor
from gollm.openai.entities import Toolset, Tool


def sample_tool_func(x):
    return x * 2


class TestToolsetAndAgentExecutor(unittest.TestCase):
    def setUp(self):
        self.sample_tool = Tool(
            name="sample_tool",
            args=["x"],
            description="Doubles the input",
            func=sample_tool_func,
            input_type=int,
        )
        self.toolset = Toolset(tools=[self.sample_tool])
        self.agent_executor = AgentExecutor(toolset=self.toolset)

    def test_add_tool(self):
        new_tool = Tool(
            name="new_tool",
            args=["y"],
            description="New tool",
            func=lambda y: y + 1,
            input_type=int,
        )
        self.toolset.add_tool(new_tool)
        print(self.toolset.get_tool_names())
        self.assertIn("new_tool", self.toolset.get_tool_names())

    def test_run_tool(self):
        agent_action = {"action": "sample_tool", "action_input": 10}
        result = self.agent_executor.execute(agent_action)
        self.assertEqual(
            result, {"tool_name": "sample_tool", "tool_output": 20, "tool_input": 10}
        )

    def test_run_nonexistent_tool(self):
        agent_action = {"action": "nonexistent_tool", "action_input": 10}
        with self.assertRaises(KeyError):
            self.agent_executor.execute(agent_action)


if __name__ == "__main__":
    unittest.main()
