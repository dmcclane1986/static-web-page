import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HTMLNode("div")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_one_prop(self):
        # Test with a single property
        node = HTMLNode("a", props={"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com"')
        
    def test_props_to_html_with_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode(
            "a", 
            props={
                "href": "https://www.example.com", 
                "target": "_blank"
            }
        )
        # Note: Since dictionaries are unordered, the order of attributes might vary
        # We can check if both attributes are in the result
        result = node.props_to_html()
        self.assertIn(' href="https://www.example.com"', result)
        self.assertIn(' target="_blank"', result)
        # Check the total length to ensure no extra attributes
        self.assertEqual(len(result), len(' href="https://www.example.com" target="_blank"'))

if __name__ == "__main__":
    unittest.main()