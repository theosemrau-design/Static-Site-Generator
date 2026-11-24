import unittest
from converter import text_to_textnodes, markdown_to_blocks, markdown_to_html_node
from textnode import TextNode, TextType

class TestConverter(unittest.TestCase):
    def test_text_to_textnodes(self) -> None:
        result: list[TextNode] = text_to_textnodes(text="This is **text** _and_ `code` and [links](https.//www.google.com) and ![images](https://i.imgur.com/zjjcJKZ.png)")
        expected: list[TextNode] = [
            TextNode(content="This is ", text_type=TextType.TEXT),
            TextNode(content="text", text_type=TextType.BOLD),
            TextNode(content=" ", text_type=TextType.TEXT),
            TextNode(content="and", text_type=TextType.ITALIC),
            TextNode(content=" ", text_type=TextType.TEXT),
            TextNode(content="code", text_type=TextType.CODE),
            TextNode(content=" and ", text_type=TextType.TEXT),
            TextNode(content="links", text_type=TextType.LINK, url="https.//www.google.com"),
            TextNode(content=" and ", text_type=TextType.TEXT),
            TextNode(content="images", text_type=TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png")
        ]
        self.assertEqual(result, expected)

    def test_markdown_to_blocks(self) -> None:
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_paragraphs(self) -> None:
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self) -> None:
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self) -> None:
        md = """
> this is a quote _with_ **different**
> `types` of text.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
             html,
             "<div><blockquote>this is a quote <i>with</i> <b>different</b> <code>types</code> of text.</blockquote></div>"
        )

    def test_heading(self) -> None:
        md = """
## this _is_ **a** `heading`.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
             html,
             "<div><h2>this <i>is</i> <b>a</b> <code>heading</code>.</h2></div>"
        )

    def test_unordered_list(self) -> None:
        md = """
- this is **a** list _item_
- this is another `list` item
- this too
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is <b>a</b> list <i>item</i></li><li>this is another <code>list</code> item</li><li>this too</li></ul></div>"
            )

    def test_ordered_list(self) -> None:
        md = """
1. idk
2. `me` _too_
3. **bold** thing
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>idk</li><li><code>me</code> <i>too</i></li><li><b>bold</b> thing</li></ol></div>"
        )


if __name__ == "__main__":
    unittest.main()