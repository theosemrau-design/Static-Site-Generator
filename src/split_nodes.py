import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str | None = None, text_type: TextType | None = None) -> list[TextNode]:
    if not delimiter or not text_type:
        return old_nodes
    nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            nodes.append(old_node)
            continue
        split_old_nodes: list[str] = old_node.content.split(delimiter)
        if len(split_old_nodes) % 2 == 0:
            raise ValueError(f"Missing closing delimiter: {delimiter} in {old_node.content}")
        for i, content in enumerate(split_old_nodes):
            if len(content) == 0:
                continue
            if i % 2 == 0:
                nodes.append(TextNode(content=content, text_type=TextType.TEXT))
                continue
            nodes.append(TextNode(content=content, text_type=text_type))
    return nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            nodes.append(old_node)
            continue
        images: list[tuple[str, str]] = extract_markdown_images(old_node.content)
        if len(images) == 0:
            nodes.append(old_node)
            continue
        content: str = old_node.content
        sections: list[str] = []
        for i, img in enumerate(images):
            alt_text, link = img
            split_content: list[str] = content.split(f"![{alt_text}]({link})", 1)
            sections.append(split_content[0])
            content = split_content[1]
        for i, text in enumerate(sections):
            alt_text, link = images[i]
            if len(text) > 0:
                nodes.append(TextNode(content=text, text_type=TextType.TEXT))
            nodes.append(TextNode(content=alt_text, text_type=TextType.IMAGE, url=link))
        if len(content) > 0:
            nodes.append(TextNode(content=content, text_type=TextType.TEXT))
    return nodes
        

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            nodes.append(old_node)
            continue
        links: list[tuple[str, str]] = extract_markdown_links(old_node.content)
        if len(links) == 0:
            nodes.append(old_node)
            continue
        content: str = old_node.content
        sections: list[str] = []
        for i, img in enumerate(links):
            alt_text, link = img
            split_content: list[str] = content.split(f"[{alt_text}]({link})", 1)
            sections.append(split_content[0])
            content = split_content[1]
        for i, text in enumerate(sections):
            alt_text, link = links[i]
            if len(text) > 0:
                nodes.append(TextNode(content=text, text_type=TextType.TEXT))
            nodes.append(TextNode(content=alt_text, text_type=TextType.LINK, url=link))
        if len(content) > 0:
            nodes.append(TextNode(content=content, text_type=TextType.TEXT))
    return nodes