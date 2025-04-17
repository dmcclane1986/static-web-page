from textnode import *
import re


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

