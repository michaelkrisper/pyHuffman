# pyHuffman

Huffman coding in a single, dependency-free Python module - build the code, encode, decode, and see how much it saves.

[![CI](https://github.com/michaelkrisper/pyHuffman/actions/workflows/ci.yml/badge.svg)](https://github.com/michaelkrisper/pyHuffman/actions/workflows/ci.yml)
[![Version](https://img.shields.io/github/v/tag/michaelkrisper/pyHuffman?sort=semver&label=version)](https://github.com/michaelkrisper/pyHuffman/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

## Features

- Builds an optimal prefix-free Huffman code from symbol frequencies (min-heap based)
- Works on `str` (per character, full Unicode) and `bytes` (per byte, any binary file)
- Packs the bit stream into bytes with a 4-byte header holding the exact bit count
- Decodes back to the original type and verifies the round trip
- Command-line demo that prints the code table and compression statistics
- Standard library only

## Usage

### Command line

```bash
python3 huffman.py                # encode a built-in Lorem Ipsum sample
python3 huffman.py testdata.html  # encode any file (read as bytes)
```

The script prints each symbol's code (shortest first) followed by statistics:

```
Code Length (bits): 27728
Original Text Length (bits): 839728
Encoded Text Length (bits): 511880
Compression Percentage: 61.0%
Compression Percentage (with code): 64.3%
```

"with code" adds the size of the code table, which a decoder would need as well.

### Library

```python
from huffman import decode_data, encode_data, get_huffman_code

text = "abracadabra"
code = get_huffman_code(text)        # {'a': (0,), 'd': (1, 0, 0), ...}
encoded = encode_data(text, code)    # bytes: 4-byte bit count + packed bits
assert decode_data(encoded, code) == text
```

The code table is not embedded in the encoded output; keep it alongside the data.

## Development

```bash
pip install pytest ruff
pytest      # run the test suite
ruff check  # lint
```

CI runs both on every push and pull request against Python 3.9 to 3.14.
Every merge to `main` is tagged with the next patch version; bundled releases
with release notes come from the Release workflow.

## Project structure

| File | Purpose |
| --- | --- |
| `huffman.py` | Tree construction, encoder, decoder and CLI |
| `test_huffman.py` | Unit tests: round trips, code properties, edge cases |
| `testdata.html`, `testimage.jpg` | Sample inputs for text and binary encoding |

## Contributing

Changes start with an issue and go through a pull request; see
[CONTRIBUTING](CONTRIBUTING.md).

## License

MIT - see [LICENSE](LICENSE).
