from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        # First check if 'other' is also a TextNode
        if not isinstance(other, TextNode):
            return False
        
        # Then compare all properties
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)

    def __repr__(self):
        # Get the string value of the enum using .value
        text_type_str = self.text_type.value
        
        # Return the formatted string
        return f"TextNode({self.text}, {text_type_str}, {self.url})"