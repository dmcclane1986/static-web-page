import unittest
from textnode import *
from converter import *


class TestConverter(unittest.TestCase):
    def test_basic_functionality(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "This is text with a "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "code block"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == " word"
        assert new_nodes[2].text_type == TextType.TEXT

    def test_multiple_delimiter_pairs(self):
        node = TextNode("Text with `code` and more `code blocks`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 4
        assert new_nodes[0].text == "Text with "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "code"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == " and more "
        assert new_nodes[2].text_type == TextType.TEXT
        assert new_nodes[3].text == "code blocks"
        assert new_nodes[3].text_type == TextType.CODE


    def test_bold_delimiter(self):
        node = TextNode("Text with **bold** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "Text with "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "bold"
        assert new_nodes[1].text_type == TextType.BOLD
        assert new_nodes[2].text == " words"
        assert new_nodes[2].text_type == TextType.TEXT

        
    def test_italic_delimiter(self):
        node = TextNode("Text with _italic_ words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "Text with "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "italic"
        assert new_nodes[1].text_type == TextType.ITALIC
        assert new_nodes[2].text == " words"
        assert new_nodes[2].text_type == TextType.TEXT

    def test_no_delimiters(self):
        node = TextNode("Plain text with no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 1
        assert new_nodes[0].text

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images_and_links(self):
        text = "Here's ![an image](http://example.com/img.jpg) and [a link](http://example.com) followed by ![another image](http://example.com/img2.png)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("an image", "http://example.com/img.jpg"), ("another image", "http://example.com/img2.png")], image_matches)
        self.assertListEqual([("a link", "http://example.com")], link_matches)

    def test_empty_text(self):
        image_matches = extract_markdown_images("This is an empty alt text image: ![](https://example.com/img.jpg)")
        link_matches = extract_markdown_links("This is an empty anchor text link: [](https://example.com)")
        self.assertListEqual([("", "https://example.com/img.jpg")], image_matches)
        self.assertListEqual([("", "https://example.com")], link_matches)
    
    def test_complex_urls(self):
        image_matches = extract_markdown_images("![image](https://example.com/path?query=value&another=123)")
        link_matches = extract_markdown_links("[link](https://example.com/path?query=value&another=123)")
        self.assertListEqual([("image", "https://example.com/path?query=value&another=123")], image_matches)
        self.assertListEqual([("link", "https://example.com/path?query=value&another=123")], link_matches)

    def test_no_matches(self):  
        # Text without any markdown images
        image_matches = extract_markdown_images("This is plain text with no images or links.")
        self.assertListEqual([], image_matches)
        
        # Text without any markdown links
        link_matches = extract_markdown_links("This is plain text with no images or links.")
        self.assertListEqual([], link_matches)
        
        # Text with a malformed image tag
        image_matches = extract_markdown_images("This has a broken image tag: !image.jpg")
        self.assertListEqual([], image_matches)
        
        # Text with a malformed link tag
        link_matches = extract_markdown_links("This has a broken link tag: [link](broken")
        self.assertListEqual([], link_matches)


    def test_split_nodes_image(self):
        # Test case provided in the assignment
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_nodes_image_no_images(self):
        # Test case with no images
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_nodes_image_multiple_nodes(self):
        # Test with multiple input nodes
        node1 = TextNode("Text with ![img1](url1)", TextType.TEXT)
        node2 = TextNode("Another text", TextType.TEXT)
        node3 = TextNode("Text with ![img2](url2) and ![img3](url3)", TextType.TEXT)
        
        new_nodes = split_nodes_image([node1, node2, node3])
        
        expected_nodes = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            node2,  # This node has no images, so it should remain unchanged
            TextNode("Text with ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img3", TextType.IMAGE, "url3"),
        ]
    
        self.assertListEqual(expected_nodes, new_nodes) 


    def test_split_nodes_link(self):
        # Test case provided in the assignment
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/) and another [second link](https://i.imgur.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/"
                ),
            ],
            new_nodes,
        )
        
    def test_split_nodes_link_no_links(self):
        # Test case with no links
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_nodes_link_multiple_nodes(self):
        # Test with multiple input nodes
        node1 = TextNode("Text with [link1](url1)", TextType.TEXT)
        node2 = TextNode("Another text", TextType.TEXT)
        node3 = TextNode("Text with [link2](url2) and [link3](url3)", TextType.TEXT)
        
        new_nodes = split_nodes_link([node1, node2, node3])
        
        expected_nodes = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            node2,  # This node has no links, so it should remain unchanged
            TextNode("Text with ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link3", TextType.LINK, "url3"),
        ]
    
        self.assertListEqual(expected_nodes, new_nodes) 

    def test_text_to_textnodes_simple(self):
        # Test with plain text
        text = "Just plain text"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 1
        assert nodes[0].text == "Just plain text"
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[0].url is None

    def test_text_to_textnodes_bold(self):
        # Test with bold text
        text = "This has a **bold** word"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[0].text == "This has a "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "bold"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == " word"
        assert nodes[2].text_type == TextType.TEXT

    def test_text_to_textnodes_mixed(self):
        # Test with multiple formatting elements
        text = "This has **bold** and _italic_ and `code`"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 6
        # Verify each node...

    def test_text_to_textnodes_with_links(self):
        # Test with a link
        text = "Click [here](https://boot.dev) to learn"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[1].text == "here"
        assert nodes[1].text_type == TextType.LINK
        assert nodes[1].url == "https://boot.dev"

    def test_text_to_textnodes_with_images(self):
        # Test with an image
        text = "See this ![cool image](https://example.com/img.jpg)"

    

if __name__ == "__main__":
    unittest.main()
