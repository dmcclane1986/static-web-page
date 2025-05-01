import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_simple_title(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")
    
    def test_extract_title_with_whitespace(self):
        markdown = "#    Title with spaces    "
        self.assertEqual(extract_title(markdown), "Title with spaces")
    
    def test_extract_title_from_multiple_lines(self):
        markdown = "Some text\n# The Real Title\nMore text"
        self.assertEqual(extract_title(markdown), "The Real Title")
    
    def test_no_title_raises_exception(self):
        markdown = "No title here\nJust regular text"
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_ignore_secondary_headers(self):
        markdown = "## Secondary header\n### Tertiary header"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == '__main__':
    unittest.main()