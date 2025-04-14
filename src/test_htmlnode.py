import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("span","Here we go")
        self.assertEqual(node.to_html(), "<span>Here we go</span>")
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "I am here")
        self.assertEqual(node.to_html(), "I am here")
    
    def test_leaf_to_html_no_value(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_to_html_empty_value(self):
        node = LeafNode("a", "")
        self.assertEqual(node.to_html(), "<a></a>")

    def test_leaf_to_html_with_single_property(self):
        node = LeafNode("a", "Click me", {"href":"https://example.com"})

        result = node.to_html()
        
        self.assertEqual(result, '<a href="https://example.com">Click me</a>')

    def test_leaf_to_html_with_multiple_properties(self):
    # Arrange: Create a leaf node with multiple properties
        props = {
            "class": "btn primary",
            "id": "submit-button",
            "data-test": "login-btn"
        }
        node = LeafNode("button", "Submit", props)
        
        # Act: Generate the HTML
        result = node.to_html()
        
        self.assertEqual(len(result), len('<button class="btn primary" id="submit-button" data-test="login-btn">Submit</button>'))


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()