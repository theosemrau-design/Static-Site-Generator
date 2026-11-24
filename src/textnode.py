from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    def __init__(self, content: str, text_type: TextType, url: str | None = None) -> None:
        self.content: str = content
        self.text_type: TextType = text_type
        self.url: str|None = url

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, TextNode):
            return False
        return self.content == value.content and self.text_type == value.text_type and self.url == value.url

    def __repr__(self) -> str:
        return f"TextNode({self.content}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.content)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.content)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.content)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.content)
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("Link tag specified but url missing")
            return LeafNode(tag="a", value=text_node.content, props={"href": text_node.url})
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError("Image tag specified but url missing")
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.content})
        case _:
            raise Exception("Text Node not found")