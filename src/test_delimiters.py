import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links,split_nodes_image, split_nodes_link

class TestDelimiters(unittest.TestCase):
    def test_one_delimiter(self) -> None:
        node: TextNode = TextNode(content="This is **bold** text.", text_type=TextType.TEXT)
        result: list[TextNode] = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        expected: list[TextNode] = [
            TextNode(content="This is ", text_type=TextType.TEXT),
            TextNode(content="bold", text_type=TextType.BOLD),
            TextNode(content=" text.", text_type=TextType.TEXT)
            ]
        self.assertEqual(result, expected)

    def test_different_delimiters(self) -> None:
        bold: TextNode = TextNode(content="This is **bold** text.", text_type=TextType.TEXT)
        italic: TextNode = TextNode(content="This is _italic_ text.", text_type=TextType.TEXT)
        code: TextNode = TextNode(content="This is `Code` text.", text_type=TextType.TEXT)
        result_bold: list[TextNode] = split_nodes_delimiter(old_nodes=[bold], delimiter="**", text_type=TextType.BOLD)
        result_italic: list[TextNode] = split_nodes_delimiter(old_nodes=[italic], delimiter="_", text_type=TextType.ITALIC)
        result_code: list[TextNode] = split_nodes_delimiter(old_nodes=[code], delimiter="`", text_type=TextType.CODE)
        expected_bold: list[TextNode] = [
            TextNode(content="This is ", text_type=TextType.TEXT),
            TextNode(content="bold", text_type=TextType.BOLD),
            TextNode(content=" text.", text_type=TextType.TEXT)
        ]
        expected_italic: list[TextNode] = [
            TextNode(content="This is ", text_type=TextType.TEXT),
            TextNode(content="italic", text_type=TextType.ITALIC),
            TextNode(content=" text.", text_type=TextType.TEXT)
        ]
        expected_code: list[TextNode] = [
            TextNode(content="This is ", text_type=TextType.TEXT),
            TextNode(content="Code", text_type=TextType.CODE),
            TextNode(content=" text.", text_type=TextType.TEXT)
        ]
        self.assertEqual(result_bold, expected_bold)
        self.assertEqual(result_italic, expected_italic)
        self.assertEqual(result_code, expected_code)

    def test_outer_delimiters(self) -> None:
        start: TextNode = TextNode(content="**bold** right at the start.", text_type=TextType.TEXT)
        end: TextNode = TextNode(content="at the end you'll find **bold**", text_type=TextType.TEXT)
        both: TextNode = TextNode(content="**Bold** at the start and also at the **End?**", text_type=TextType.TEXT)
        result_start: list[TextNode] = split_nodes_delimiter([start], "**", TextType.BOLD)
        result_end: list[TextNode] = split_nodes_delimiter([end], "**", TextType.BOLD)
        result_both: list[TextNode] = split_nodes_delimiter([both], "**", TextType.BOLD)
        expected_start: list[TextNode] = [
            TextNode(content="bold", text_type=TextType.BOLD),
            TextNode(content=" right at the start.", text_type=TextType.TEXT)
        ]
        expected_end: list[TextNode] = [
            TextNode(content="at the end you'll find ", text_type=TextType.TEXT),
            TextNode(content="bold", text_type=TextType.BOLD)
        ]
        expected_both: list[TextNode] = [
            TextNode(content="Bold", text_type=TextType.BOLD),
            TextNode(content=" at the start and also at the ", text_type=TextType.TEXT),
            TextNode(content="End?", text_type=TextType.BOLD),
        ]
        self.assertEqual(result_start, expected_start)
        self.assertEqual(result_end, expected_end)
        self.assertEqual(result_both, expected_both)

    def test_no_delimiter(self) -> None:
        node = TextNode(content="No delimiter here.", text_type=TextType.TEXT)
        result: list[TextNode] = split_nodes_delimiter(old_nodes=[node])
        expected: list[TextNode] = [node]
        self.assertEqual(result, expected)

    def test_non_text_nodes(self) -> None:
        node = TextNode(content="Already bolded.", text_type=TextType.BOLD)
        result: list[TextNode] = split_nodes_delimiter(old_nodes=[node], delimiter="_", text_type=TextType.ITALIC)
        expected: list[TextNode] = [node]
        self.assertEqual(result, expected)

    def test_error(self) -> None:
        node = TextNode(content="This is **bold forgot to be closed", text_type=TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)

    def test_multiple_pairs(self) -> None:
        node = TextNode(content="This `has` multiple `Code` blocks", text_type=TextType.TEXT)
        result: list[TextNode] = split_nodes_delimiter(old_nodes=[node], delimiter="`", text_type=TextType.CODE)
        expected: list[TextNode] = [
            TextNode(content="This ", text_type=TextType.TEXT),
            TextNode(content="has", text_type=TextType.CODE),
            TextNode(content=" multiple ", text_type=TextType.TEXT),
            TextNode(content="Code", text_type=TextType.CODE),
            TextNode(content=" blocks", text_type=TextType.TEXT)
            ]
        self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        multiple_matches = extract_markdown_images(
            "This is text with ![python](https://i.imgur.com/zjjcJKZ.png) and ![memes](https://imgur.com/gallery/kid-fucker-couch-fucker-7HYxFM6#f3UL6wI)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        self.assertListEqual([("python", "https://i.imgur.com/zjjcJKZ.png"), ("memes", "https://imgur.com/gallery/kid-fucker-couch-fucker-7HYxFM6#f3UL6wI")], multiple_matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://fnf-2.io)"
        )
        multiple_matches = extract_markdown_links(
            "This is text with [fnf](https://fnf-2.io) and [google](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://fnf-2.io")], matches)
        self.assertListEqual([("fnf", "https://fnf-2.io"), ("google", "https://www.google.com")], multiple_matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://fnf-2.io) and another [google link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://fnf-2.io"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("google link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
