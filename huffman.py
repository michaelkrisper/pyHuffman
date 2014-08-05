#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example script for encoding/decoding data with Huffman-coding
Usage:
1) with default lorem-ipsum text: python huffman.py
2) with an input file to encode:  python huffman.py <inputfile>
"""

import Queue
import collections
import heapq
import sys

__author__ = "Michael Krisper"
__email__ = "michael.krisper@gmail.com"
__date__ = "2014-08-05"

class TreeNode(object):
    def __init__(self, value=None, count=1, left=None, right=None, code = ""):
        self.count = count
        self.value = value
        self.left = left
        self.right = right
        self.code = code

    def isLeaf(self):
        return not (self.left or self.right)

    def __lt__(self, other):
        return self.count < other.count

    def __add__(self, other):
        self.code = 0
        other.code = 1
        return TreeNode(None, self.count + other.count, self, other)

    def __repr__(self):
        return "TreeNode(%r, %r)" % (self.value, self.count)

def convert_huffman_tree_to_code(node, prefix=[]):
    """Traverses all nodes in a tree and converts it to a code."""
    code = {}
    if node:
        prefix = prefix + [node.code]
        if node.isLeaf():
            code[node.value] = prefix
        else:
            code.update(convert_huffman_tree_to_code(node.left, prefix))
            code.update(convert_huffman_tree_to_code(node.right, prefix))
    return code

def get_huffman_code(text):
    """Returns a Code-Dictionary { key=Character, value=Code }"""

    counter = collections.Counter(text)
    heap = [TreeNode(item, count) for item,count in counter.iteritems()]

    heapq.heapify(heap)
    
    while len(heap) >= 2:
        heapq.heappush(heap, heapq.heappop(heap)+heapq.heappop(heap))

    tree = heap[0]    
    return convert_huffman_tree_to_code(tree)

def encrypt_text(text, code):
    """Encrypts a text with huffman-code"""
    crypted = []
    for char in text:
        crypted.extend(code[char])

    return "".join(str(v) for v in crypted)

def decrypt_text(text, code):
    """Decrypts a text with huffman-code"""
    decrypted = []
    reverse_code = dict(zip(["".join([str(y) for y in v]) for v in code.values()], code.keys()))

    current = ""
    for c in text:
        current += c
        if current in reverse_code:
            decrypted.append(reverse_code[current])
            current = ""
    return "".join(decrypted)

def main(text):
    """Shows sample usage of the functions for the Huffman-code."""

    code = get_huffman_code(text)
    
    # print the code
    for key, value in sorted(code.iteritems(), key=lambda (k, v): (len(v), k)):
        print "%s: %s" % (key, "".join(str(v) for v in value))

    crypted_text = encrypt_text(text, code)
    decrypted_text = decrypt_text(crypted_text, code)
    assert decrypted_text == text
    
    code_text = str(code)
    result = (len(code_text),
              len(text) * 8, len(crypted_text),
              len(crypted_text) / (len(text) * 8.0) * 100,
              len(crypted_text + code_text) / (len(text) * 8.0) * 100)
    print "Code Length: %d, Text Length: %d, Encrypted Text Length: %d - Percentage: %.1f %% / (%.1f %% with Code)" % result

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
