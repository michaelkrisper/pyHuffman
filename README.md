# pyHuffman

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A Python script for illustrating the encoding and decoding of data using Huffman coding. This script can handle both text and binary files.

## Description

This project is a Python 3 implementation of the Huffman coding algorithm. It includes a script (`huffman.py`) that can be used to compress and decompress data. The script has been refactored for clarity and now includes comprehensive documentation and a test suite.

## Usage

You can run the script from the command line. You can either provide a file as an argument for encoding or run it without arguments to use a default sample text.

### With Default Text

To run the script with the default Lorem Ipsum text, simply execute:

```bash
python3 huffman.py
```

### With a File

To encode a specific file, provide the file path as a command-line argument:

```bash
python3 huffman.py [file_path]
```

For example, to encode the provided `testdata.html`:

```bash
python3 huffman.py testdata.html
```

## Testing

A test suite is included to verify the functionality of the Huffman coding implementation. The tests cover various scenarios, including simple text, empty strings, and different file types.

To run the tests, execute the following command from the root directory:

```bash
python3 -m unittest test_huffman.py
```

You should see an output indicating that all tests passed successfully.

## Requirements

- Python 3.9 or newer — standard library only

## Project structure

| File | Purpose |
|---|---|
| `huffman.py` | Encoder, decoder, tree construction and CLI |
| `test_huffman.py` | Unit tests covering text, binary and edge cases |
| `testdata.html`, `testimage.jpg` | Sample inputs for text and binary encoding |

## License

MIT — see [LICENSE](LICENSE).
