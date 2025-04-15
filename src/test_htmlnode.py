import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


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
    def test_to_html_with_empty_children_list(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "first")
        child2 = LeafNode("b", "second")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><span>first</span><b>second</b></div>")
    
    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(parent.to_html(), '<div class="container" id="main"><span>child</span></div>')

    def test_to_html_with_missing_tag(self):
        child = LeafNode("span", "child")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_with_none_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()
    
    def test_deep_nesting(self):
        leaf = LeafNode("b", "text")
        parent1 = ParentNode("p", [leaf])
        parent2 = ParentNode("div", [parent1])
        parent3 = ParentNode("section", [parent2])

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("print('Hello World')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello World')")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("Image description", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Image description"})

    def test_invalid_type_class(self):

        class InvalidNode:
            def __init__(self):
                self.text = "Invalid node"
                self.text_type = "INVALID_TYPE"  
        
        invalid_node = InvalidNode()
        

        with self.assertRaises(Exception):
            text_node_to_html_node(invalid_node)
    def test_invalid_type(self):

        invalid_node = TextNode("Test", "NOT_A_VALID_TYPE")
        
        with self.assertRaises(Exception):
            text_node_to_html_node(invalid_node)

if __name__ == "__main__":
    unittest.main()