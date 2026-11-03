import contextlib
import io
import struct
import unittest
from pathlib import Path

from huffman import decode_data, encode_data, get_huffman_code, run

HERE = Path(__file__).parent


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
        file_path = HERE / "testdata.html"
        with open(file_path, encoding="utf-8") as f:
            text = f.read()

        code = get_huffman_code(text)
        encoded = encode_data(text, code)
        decoded = decode_data(encoded, code)
        self.assertEqual(text, decoded)

    def test_binary_file(self):
        """Tests encoding and decoding of a binary file."""
        file_path = HERE / "testimage.jpg"
        with open(file_path, "rb") as f:
            data = f.read()

        code = get_huffman_code(data)
        encoded = encode_data(data, code)
        decoded = decode_data(encoded, code)
        self.assertEqual(data, decoded)

    def test_known_code_lengths(self):
        """The most frequent symbol gets the shortest code."""
        code = get_huffman_code("aaaabbc")
        self.assertEqual(len(code["a"]), 1)
        self.assertEqual(len(code["b"]), 2)
        self.assertEqual(len(code["c"]), 2)

    def test_code_is_prefix_free(self):
        code = get_huffman_code("the quick brown fox jumps over the lazy dog")
        words = ["".join(map(str, bits)) for bits in code.values()]
        for a in words:
            for b in words:
                if a != b:
                    self.assertFalse(b.startswith(a), f"{a} is a prefix of {b}")

    def test_code_satisfies_kraft_equality(self):
        """A full binary Huffman tree uses the whole code space."""
        code = get_huffman_code("abracadabra alakazam")
        self.assertAlmostEqual(sum(2 ** -len(bits) for bits in code.values()), 1.0)

    def test_encoded_size_is_optimal(self):
        """Huffman coding never needs more bits than a fixed-length code."""
        text = "mississippi river"
        code = get_huffman_code(text)
        encoded = encode_data(text, code)
        num_bits = struct.unpack(">L", encoded[:4])[0]
        self.assertEqual(num_bits, sum(len(code[c]) for c in text))
        fixed_bits = len(text) * (len(code) - 1).bit_length()
        self.assertLessEqual(num_bits, fixed_bits)

    def test_header_and_padding(self):
        encoded = encode_data("aaaabbc", get_huffman_code("aaaabbc"))
        # 4 + 2 * 2 + 2 = 10 bits -> 4 byte header + 2 data bytes
        self.assertEqual(struct.unpack(">L", encoded[:4])[0], 10)
        self.assertEqual(len(encoded), 6)

    def test_unicode_text(self):
        text = "Grüße aus Österreich - 日本語 - emoji \U0001F600"
        code = get_huffman_code(text)
        self.assertEqual(decode_data(encode_data(text, code), code), text)

    def test_all_byte_values(self):
        data = bytes(range(256)) * 3 + b"\x00" * 100
        code = get_huffman_code(data)
        self.assertEqual(len(code), 256)
        self.assertEqual(decode_data(encode_data(data, code), code), data)

    def test_single_byte_value(self):
        data = b"\xff" * 9
        code = get_huffman_code(data)
        self.assertEqual(decode_data(encode_data(data, code), code), data)

    def test_run_prints_statistics(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            run("hello huffman")
        self.assertIn("Compression Percentage", out.getvalue())


if __name__ == "__main__":
    unittest.main()
