

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = "" 
        for prop, value in self.props.items():
            props_html += f' {prop}="{value}"'
        return props_html
        
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
                
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        if self.tag is None:
            return self.value
        
        attrs_str = ""
        if self.props:
            for attr, value in self.props.items():
                attrs_str += f' {attr}="{value}"'
        return f"<{self.tag}{attrs_str}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None ):
        super().__init__(tag, value=None, children=children, props= props )

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNod is missing a tag")
        if self.children == None:
            raise ValueError("ParentNode is missing required children")
        html = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"


        return html