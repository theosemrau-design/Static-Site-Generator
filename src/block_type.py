from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def block_to_block_type(markdown: str) -> BlockType:
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE

    heading: bool = True
    quote: bool = True
    unordered_list: bool = True
    ordered_list: bool = True
    for i, line in enumerate(markdown.split("\n")):
        hashtags: int = 0
        while hashtags < len(line) and line[hashtags] == "#":
            hashtags += 1
        if hashtags == 0 or hashtags > 6 or hashtags >= len(line) or line[hashtags] != " ":
            heading = False
        if not line.startswith(">"):
            quote = False
        if not line.startswith("- "):
            unordered_list = False
        if not line.startswith(f"{i + 1}. "):
            ordered_list = False
    if heading:
        return BlockType.HEADING
    if quote:
        return BlockType.QUOTE
    if unordered_list:
        return BlockType.UNORDERED_LIST
    if ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH