class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children = None, props: dict[str, str] | None = None) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: dict[str, str] | None = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props or len(self.props) == 0:
            return ""

        result_string: str = ""
        for prop, value in self.props.items():
            result_string += f' {prop}="{value}"'

        return result_string

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.value or self.value == None:
            raise ValueError("All leaf nodes must hava a value")
        if not self.tag or self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag or self.tag == None:
            raise ValueError("All parent nodes need to hava a tag")
        if not self.children or self.children == None:
            raise ValueError("All parent nodes need to hava children")

        return_string: str = ""
        for child in self.children:
            return_string += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{return_string}</{self.tag}>"