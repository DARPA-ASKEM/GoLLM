from core.utils import remove_references, extract_json
import unittest


class TestRemoveReferences(unittest.TestCase):

	def test_remove_without_following_section(self):
		text = """
		Some initial text.
		References
		1. Reference one details.
		2. Reference two details.
		"""
		result = remove_references(text)
		self.assertNotIn("References", result)
		self.assertIn("Some initial text.", result)

	def test_no_references_section(self):
		text = """
		Some initial text.
		No references here.
		"""
		result = remove_references(text)
		self.assertEqual(text.strip(), result)


class TestExtractJson(unittest.TestCase):

	def test_valid_json(self):
		"""Test with a valid JSON embedded in garbage text."""
		input_str = "GARBAGE!{\"key\": \"value\"}MOREGARBAGE"
		expected = {"key": "value"}
		self.assertEqual(extract_json(input_str), expected)

	def test_invalid_json(self):
		"""Test with invalid JSON (missing closing brace)."""
		input_str = "GARBAGE!{\"key\": \"value\"MOREGARBAGE"
		self.assertIsNone(extract_json(input_str))

	def test_no_json(self):
		"""Test with no JSON present in the text."""
		input_str = "Just some random text without JSON"
		self.assertIsNone(extract_json(input_str))

	def test_nested_complex_json(self):
		"""Test with a nested and more complex JSON structure."""
		input_str = 'GARBAGE!{"name": "John", "age": 30, "cars": {"car1": {"make": "Ford", "model": "Fiesta"}, "car2": {"make": "BMW", "model": "X5"}}, "children": [{"name": "Alice", "age": 5}, {"name": "Bob", "age": 7}]}GARBAGE'
		expected = {
			"name": "John",
			"age": 30,
			"cars": {
				"car1": {"make": "Ford", "model": "Fiesta"},
				"car2": {"make": "BMW", "model": "X5"}
			},
			"children": [
				{"name": "Alice", "age": 5},
				{"name": "Bob", "age": 7}
		]
	}
		self.assertEqual(extract_json(input_str), expected)

	def test_json_with_curly_braces(self):
		"""Test with JSON containing curly braces in strings."""
		input_str = r'GARBAGE!{"key": "{value}"}GARBAGE'
		expected = {"key": "{value}"}
		self.assertEqual(extract_json(input_str), expected)

	def test_empty_string(self):
		"""Test with an empty string."""
		input_str = ""
		self.assertIsNone(extract_json(input_str))


if __name__ == '__main__':
	unittest.main()
