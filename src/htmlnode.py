class HTMLNode:
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
        temp1 = []
        for key, value in self.props.items():
            temp1.append(f' {key}="{value}"')
        temp2 = "".join(temp1)
        return temp2
    
    def __repr__(self):
        print(self.tag)
        print(self.value)
        print(self.children)
        print(self.props)

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

        
    def to_html(self):
        if self.value is None:
            raise ValueError ("No value given")
        if self.tag is None or self.tag == "":
            return self.value
        if self.tag == "img":
            formatted_props = self.props_to_html()
            return f"<img{formatted_props}>"
        formatted_props = self.props_to_html()
        return f"<{self.tag}{formatted_props}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError ("No tag given")
        if self.children is None:
            raise ValueError ("No children given")
        if self.value is not None:
            raise ValueError ("Value present")
        formatting_props = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{formatting_props}>{children_html}</{self.tag}>"