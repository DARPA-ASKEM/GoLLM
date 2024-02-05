from core.utils import remove_references
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

if __name__ == '__main__':
    unittest.main()
