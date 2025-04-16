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

if __name__ == "__main__":
    unittest.main()
