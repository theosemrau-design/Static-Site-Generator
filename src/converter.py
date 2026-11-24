from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from block_type import block_to_block_type, BlockType
from split_nodes import split_nodes_delimiter, split_nodes_link, split_nodes_image

def text_to_textnodes(text: str) -> list[TextNode]:
    old_nodes: list[TextNode] = [TextNode(content=text, text_type=TextType.TEXT)]
    bold1: list[TextNode] = split_nodes_delimiter(old_nodes=old_nodes, delimiter="**", text_type=TextType.BOLD)
    italic2: list[TextNode] = split_nodes_delimiter(old_nodes=bold1, delimiter="_", text_type=TextType.ITALIC)
    code3: list[TextNode] = split_nodes_delimiter(old_nodes=italic2, delimiter="`", text_type=TextType.CODE)
    link4: list[TextNode] = split_nodes_link(old_nodes=code3)
    all: list[TextNode] = split_nodes_image(old_nodes=link4)
    return all

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes: list[TextNode] = text_to_textnodes(text=text)
    html_nodes: list[HTMLNode] = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    split_markdown: list[str] = markdown.strip(" ").split("\n\n")
    new_markdown: list[str] = []
    for i in split_markdown:
        i = i.strip()
        if len(i) > 0:
            new_markdown.append(i)
    return new_markdown

def heading_to_html_node(block: str) -> HTMLNode:
    hashtags: int = len(block) - len(block.lstrip("#"))
    return ParentNode(tag=f"h{hashtags}", children=text_to_children(block.lstrip("#").lstrip(" ")))

def markdown_to_html_node(markdown: str) -> ParentNode:
    split_markdown = markdown_to_blocks(markdown=markdown)
    nodes: list[HTMLNode] = []
    for block in split_markdown:
        block_type = block_to_block_type(markdown=block)
        match block_type:
            case BlockType.QUOTE:
                clean_block_list: list[str] = []
                for i in block.split("\n"):
                    clean_block_list.append(i.removeprefix(">").removeprefix(" "))
                clean_block: str = " ".join(clean_block_list)
                block_node: HTMLNode = ParentNode(tag="blockquote",children=text_to_children(text=clean_block))
            case BlockType.UNORDERED_LIST:
                list_items: list[HTMLNode] = []
                for i in block.split("\n"):
                    list_items.append(ParentNode(tag="li", children=text_to_children(i.removeprefix("- "))))
                block_node: HTMLNode = ParentNode(tag="ul", children=list_items)
            case BlockType.ORDERED_LIST:
                list_items: list[HTMLNode] = []
                for i, block_part in enumerate(block.split("\n")):
                    list_items.append(ParentNode(tag="li", children=text_to_children(block_part.removeprefix(f"{i + 1}. "))))
                block_node: HTMLNode = ParentNode(tag="ol", children=list_items)
            case BlockType.CODE:
                text_node: TextNode = TextNode(content=block.removeprefix("```\n").removesuffix("```"), text_type=TextType.CODE)
                block_node: HTMLNode = ParentNode(tag="pre", children=[text_node_to_html_node(text_node=text_node)])
            case BlockType.HEADING:
                block_node: HTMLNode = heading_to_html_node(block=block)
            case BlockType.PARAGRAPH:
                block_node: HTMLNode = ParentNode(tag="p", children=text_to_children(block.replace("\n", " ")))

        nodes.append(block_node)
    return ParentNode(tag="div", children=nodes)