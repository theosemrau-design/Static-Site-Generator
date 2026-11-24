import unittest
from block_type import block_to_block_type, BlockType

class TestBlockType(unittest.TestCase):
    def test_heading(self) -> None:
        missing_space: str = "##heading"
        full_line: str = "####"
        normal_heading: str = "###### heading this is"
        too_many: str = "####### too many hashtags"
        self.assertEqual(block_to_block_type(missing_space), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(full_line), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(too_many), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(normal_heading), BlockType.HEADING)

    def test_code(self) -> None:
        not_three_backticks: str = """``
        code
        more code```"""
        missing_new_line: str = """```code
        more code```"""
        normal_case: str = """```
        code
        more code```"""
        self.assertEqual(block_to_block_type(not_three_backticks), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(missing_new_line), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(normal_case), BlockType.CODE)

    def test_quote(self) -> None:
        normal_case: str = """> idk
>me too"""
        not_all_lines: str = """> idk
me too"""
        self.assertEqual(block_to_block_type(normal_case), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(not_all_lines), BlockType.PARAGRAPH)

    def test_unordered_list(self) -> None:
        normal_case: str = """- idk
- me too"""
        not_all_lines: str = """- idk
me too"""
        self.assertEqual(block_to_block_type(normal_case), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(not_all_lines), BlockType.PARAGRAPH)

    def test_ordered_list(self) -> None:
        normal_case: str = """1. idk
2. me too"""
        not_all_lines: str = """1. idk
me too"""
        not_right_numbered: str = """1. idk
3. me too"""
        self.assertEqual(block_to_block_type(normal_case), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(not_all_lines), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_right_numbered), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()