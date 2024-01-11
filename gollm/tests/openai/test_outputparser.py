import unittest
import regex as re
from core.openai.react import ScratchpadParser

class TestScratchpadParser(unittest.TestCase):

    def test_get_final_answer_with_no_final_answer(self):
        scratchpad = "Some text without a final answer."
        with self.assertRaises(ValueError):
            ScratchpadParser.get_final_answer(scratchpad)

    def test_get_final_answer_with_multiple_final_answers(self):
        scratchpad = "Final Answer: 42\nFinal Answer: 43"
        self.assertEqual(ScratchpadParser.get_final_answer(scratchpad), "43")

    def test_get_actions_with_no_actions(self):
        scratchpad = "Some text without actions."
        self.assertEqual(ScratchpadParser.get_actions(scratchpad), [])

    def test_get_actions_with_multiple_actions(self):
        scratchpad = "Action:\n```\n{action_data1}\n```\nAction:\n```\n{action_data2}\n```\n"
        self.assertEqual(ScratchpadParser.get_actions(scratchpad), ["{action_data1}", "{action_data2}"])

    def test_get_observations_with_no_observations(self):
        scratchpad = "Some text without observations."
        self.assertEqual(ScratchpadParser.get_observations(scratchpad), [])

    def test_get_observations_with_multiple_observations(self):
        scratchpad = "Observation: Observation 1\nThought: Some thought\nObservation: Observation 2\nThought: Some other thought"
        self.assertEqual(ScratchpadParser.get_observations(scratchpad), [" Observation 1", " Observation 2"])

    def test_get_thoughts_with_no_thoughts(self):
        scratchpad = "Some text without thoughts."
        self.assertEqual(ScratchpadParser.get_thoughts(scratchpad), [])

    def test_get_thoughts_with_multiple_thoughts(self):
        scratchpad = "Thought: Thought 1\nAction:\n```\n{action_data}\n```\nThought: Thought 2"
        self.assertEqual(ScratchpadParser.get_thoughts(scratchpad), [" Thought 1", " Thought 2"])

    def test_match_action_blob_with_invalid_action(self):
        action = "Action without proper formatting"
        with self.assertRaises(AttributeError):
            ScratchpadParser._match_action_blob(action)

if __name__ == '__main__':
    unittest.main()
