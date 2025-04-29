from textnode import *
import re
from enum import Enum
from htmlnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    
    for old_node in old_nodes:
        # If node is not TEXT type, add it directly to result
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        # Process TEXT type node
        text = old_node.text
        remaining_text = text
        current_result = []
        
        # While we can find a pair of delimiters
        while True:
            # Find the first delimiter
            start_index = remaining_text.find(delimiter)
            if start_index == -1:
                # No more delimiters found
                if remaining_text:
                    current_result.append(TextNode(remaining_text, TextType.TEXT))
                break
            
            # Text before the first delimiter
            if start_index > 0:
                current_result.append(TextNode(remaining_text[:start_index], TextType.TEXT))
            
            # Find the second delimiter
            end_index = remaining_text.find(delimiter, start_index + len(delimiter))
            if end_index == -1:
                # No closing delimiter found - this is invalid markdown
                raise ValueError(f"No closing delimiter '{delimiter}' found")
            
            # Text between delimiters (without the delimiters themselves)
            between_text = remaining_text[start_index + len(delimiter):end_index]
            current_result.append(TextNode(between_text, text_type))
            
            # Update remaining_text to be everything after the second delimiter
            remaining_text = remaining_text[end_index + len(delimiter):]
        
        result.extend(current_result)
    
    return result

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        text = old_node.text

        images = extract_markdown_images(text)

        if not images:
            result.append(old_node)
            continue

        remaining_text = text

        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"

            parts = remaining_text.split(image_markdown, 1)
        
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))

            result.append(TextNode(image_alt, TextType.IMAGE, image_url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        if remaining_text:
            result.append(TextNode(remaining_text,TextType.TEXT))
    return result

def split_nodes_link(old_nodes):
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        text = old_node.text

        links = extract_markdown_links(text)

        if not links:
            result.append(old_node)
            continue

        remaining_text = text

        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"

            parts = remaining_text.split(link_markdown, 1)
        
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))

            result.append(TextNode(link_text, TextType.LINK, link_url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        if remaining_text:
            result.append(TextNode(remaining_text,TextType.TEXT))
    return result

def text_to_textnodes(text):
    #convert text to TextNode
    #pass TextNode to split_nodes_delimiter, and split_nodes_image, and split_nodes_link

    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):

    lines = markdown.split("\n\n")
    no_space_lines = []
    for line in lines:
        no_space_line = line.strip()
        if len(no_space_line)>0:
            no_space_lines.append(no_space_line)
    return no_space_lines

def block_to_block_type(block):
    if not block:
        return BlockType.PARAGRAPH
        
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
            
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    if len(lines) > 0:
        is_ordered_list = True
        for i, line in enumerate(lines, 1):
            if not line.startswith(f"{i}. "):
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)