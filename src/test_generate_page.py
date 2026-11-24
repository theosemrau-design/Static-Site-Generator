import unittest
from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self) -> None:
        md = """
idk
idk too
 # this is da title
"""
        fail_md = """
idk
me too
no title here
"""
        self.assertEqual(extract_title(md), "this is da title")
        with self.assertRaises(Exception):
            extract_title(fail_md)


if __name__ == "__main__":
    unittest.main()