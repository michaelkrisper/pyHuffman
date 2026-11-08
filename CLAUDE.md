# CLAUDE.md

Huffman coding in one dependency-free module, `huffman.py`: build a code from symbol
frequencies, encode to packed bytes, decode, and a CLI that prints the code table and
compression stats. Python 3.9+, standard library only. Nothing is packaged or deployed.

## Commands

```bash
python3 huffman.py                 # built-in Lorem Ipsum sample (str)
python3 huffman.py testdata.html   # any file, read as bytes
pip install pytest ruff
pytest                             # test_huffman.py, ~1 s
ruff check                         # ruff.toml: E, F, W, I, UP; 120 cols; target py39
```

CI (`.github/workflows/ci.yml`) runs ruff on 3.14 and pytest on 3.9 to 3.14.

## Architecture

- `get_huffman_code(data)` -> `{symbol: (0, 1, ...)}`. Symbols are characters for
  `str` and ints for `bytes`. Built with a `heapq` of `TreeNode`s (`__lt__` by count,
  `+` merges two nodes). A single distinct symbol gets the code `(0,)`.
- `encode_data(data, code)` -> 4-byte big-endian bit count (`struct '>L'`) followed by
  the bits packed MSB first, zero-padded to a full byte.
- `decode_data(encoded, code)` rebuilds the tree from the code table, trims the padding
  using the header and returns `bytes` if the code keys are ints, else `str`.
- The code table is not stored in the encoded output; callers keep it.
- `testdata.html` and `testimage.jpg` are sample inputs used by the tests (resolved via
  `Path(__file__).parent`, so tests run from any directory). `testdata.html` is marked
  `linguist-vendored` in `.gitattributes`.

## Rules and pitfalls

- Keep the encoded format stable (header layout, bit order, padding); tests check the
  header and round trips for text, Unicode and binary input.
- The output type of `decode_data` is inferred from the key type; an empty code
  therefore decodes to `""` even for empty `bytes` input.
- `TreeNode.is_leaf()` relies on child truthiness; don't give `TreeNode` a `__len__`
  or `__bool__`.
- Stay on the 3.9 syntax level (ruff `UP` with `target-version = "py39"`: `Union`, no
  `X | Y`) and standard library only.

## Workflow

- Every change starts with a GitHub issue. Branch `<issue>-<slug>` from `main`,
  open a PR with `Closes #<issue>`. Never push to `main` directly.
- PRs auto-merge (squash) once CI and the "Linked ticket" check pass; drafts are not merged.
- Versions exist only as git tags `vX.Y.Z`. Every merge to `main` tags the next patch;
  never edit version numbers in files. Minor/major releases: Actions -> Release.
- Nothing is deployed; a merge to `main` only creates the patch tag.
- Details: CONTRIBUTING.md.
