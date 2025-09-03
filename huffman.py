#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example script for encoding/decoding data with Huffman-coding
Usage:
1) with default lorem-ipsum text: python huffman.py
2) with an input file to encode:  python huffman.py <inputfile>
"""

import collections
import heapq
import struct
import sys

class TreeNode(object):
    def __init__(self, value=None, count=1, left=None, right=None):
        self.count = count
        self.value = value
        self.left = left
        self.right = right

    def isLeaf(self):
        return not (self.left or self.right)

    def __lt__(self, other):
        return self.count < other.count

    def __add__(self, other):
        return TreeNode(None, self.count + other.count, self, other)

    def __repr__(self):
        return "TreeNode(%r, %r)" % (self.value, self.count)

def get_huffman_code(text):
    """Returns a Code-Dictionary { key=Character, value=Code }"""

    def traverse_tree(node, prefix=()):
        if node.isLeaf():
            yield (node.value, prefix)
        else:
            for v in traverse_tree(node.left, prefix + (0,)):
                yield v
            for v in traverse_tree(node.right, prefix + (1,)):
                yield v

    counter = collections.Counter(text)
    heap = [TreeNode(item, count) for item, count in counter.items()]

    heapq.heapify(heap)

    while len(heap) >= 2:
        heapq.heappush(heap, heapq.heappop(heap) + heapq.heappop(heap))

    if not heap:
        return {}

    tree = heap[0]

    if not tree.isLeaf():
        return dict(traverse_tree(tree))
    else:
        # Handle the case with a single character
        return {tree.value: (0,)}

def encrypt_text(text, code):
    """Encrypts a text with huffman-code"""
    bits = []
    for char in text:
        bits.extend(code[char])

    num_bits = len(bits)

    padding_len = (8 - num_bits % 8) % 8
    bits.extend([0] * padding_len)

    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if bits[i + j] == 1:
                byte |= (1 << (7 - j))
        byte_array.append(byte)

    # Prepend the number of bits.
    header = struct.pack('>L', num_bits)
    return header + byte_array


def decrypt_text(crypted_data, code):
    """Decrypts a text with huffman-code"""
    if not code:
        return ""

    # Unpack header
    num_bits = struct.unpack('>L', crypted_data[:4])[0]
    byte_array = crypted_data[4:]

    # Unpack bytes into bits
    bits = []
    for byte in byte_array:
        for i in range(8):
            if (byte << i) & 0x80:
                bits.append(1)
            else:
                bits.append(0)

    # Trim padding
    if num_bits:
        bits = bits[:num_bits]

    # Build the tree from the code
    tree = TreeNode()
    for char, huffman_code in code.items():
        node = tree
        for bit in huffman_code:
            if bit == 0:
                if not node.left:
                    node.left = TreeNode()
                node = node.left
            else:
                if not node.right:
                    node.right = TreeNode()
                node = node.right
        node.value = char

    # Decode by traversing the tree
    decrypted_output = []
    node = tree
    for bit in bits:
        if bit == 0:
            node = node.left
        else:
            node = node.right

        if node.isLeaf():
            decrypted_output.append(node.value)
            node = tree # Reset to root for next character

    # Check the type of the first key to determine output type
    first_key = next(iter(code.keys()), None)
    if isinstance(first_key, int):
        return bytes(decrypted_output)
    else:
        return "".join(decrypted_output)

def main(text):
    """Shows sample usage of the functions for the Huffman-code."""

    code = get_huffman_code(text)

    # print the code
    for key, value in sorted(code.items(), key=lambda item: (len(item[1]), item[0])):
        print("%s: %s" % (key, "".join(map(str, value))))

    crypted_text = encrypt_text(text, code)
    decrypted_text = decrypt_text(crypted_text, code)

    assert decrypted_text == text

    code_text = str(code)
    text_len_bits = len(text) * 8
    crypted_len_bits = len(crypted_text) * 8
    code_len_bits = len(code_text.encode('utf-8')) * 8

    result = (code_len_bits,
              text_len_bits, crypted_len_bits,
              crypted_len_bits * 100.0 / text_len_bits,
              (crypted_len_bits + code_len_bits) * 100.0 / text_len_bits)
    print("Code Length (bits): %d, Text Length (bits): %d, Encrypted Text Length (bits): %d - Percentage: %.1f %% / (%.1f %% with Code)" % result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TEXT = open(sys.argv[1], "rb").read()
    else:
        TEXT = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et 
dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd 
gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing 
elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos 
et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."""
    main(TEXT)
