import unittest
import os
from huffman import get_huffman_code, encode_data, decode_data

class TestHuffman(unittest.TestCase):

    def test_simple_text(self):
        """Tests encoding and decoding of a simple text string."""
        text = "hello world"
        code = get_huffman_code(text)
        encoded = encode_data(text, code)
        decoded = decode_data(encoded, code)
        self.assertEqual(text, decoded)

    def test_empty_string(self):
        """Tests encoding and decoding of an empty string."""
        text = ""
        code = get_huffman_code(text)
        encoded = encode_data(text, code)
        decoded = decode_data(encoded, code)
        self.assertEqual(text, decoded)

    def test_single_character(self):
        """Tests encoding and decoding of a single character string."""
        text = "a"
        code = get_huffman_code(text)
        encoded = encode_data(text, code)
        decoded = decode_data(encoded, code)
        self.assertEqual(text, decoded)

    def test_same_characters(self):
        """Tests encoding and decoding of a string with all same characters."""
        text = "aaaaa"
        code = get_huffman_code(text)
        encoded = encode_data(text, code)
        decoded = decode_data(encoded, code)
        self.assertEqual(text, decoded)

    def test_text_file(self):
        """Tests encoding and decoding of a text file."""
        file_path = "testdata.html"
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        code = get_huffman_code(text)
        encoded = encode_data(text, code)
        decoded = decode_data(encoded, code)
        self.assertEqual(text, decoded)

    def test_binary_file(self):
        """Tests encoding and decoding of a binary file."""
        file_path = "testimage.jpg"
        with open(file_path, "rb") as f:
            data = f.read()

        code = get_huffman_code(data)
        encoded = encode_data(data, code)
        decoded = decode_data(encoded, code)
        self.assertEqual(data, decoded)

if __name__ == "__main__":
    unittest.main()
