#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module for encoding/decoding Data with the Huffman-Coding"""

import Queue

__author__ = "Michael Krisper"
__email__ = "michael.krisper@htu.tugraz.at"
__date__ = "2012-05-20"

def convert_huffman_tree_to_code(node, prefix=""):
    """Traverses all nodes in a tree and converts it to a code. left=1, right=0"""
    code = {}    
    if node:
        if len(node[1]) > 0:
            code[node[1]] = prefix
        if node[2]:
            code.update(convert_huffman_tree_to_code(node[2], prefix + "1"))
        if node[3]:
            code.update(convert_huffman_tree_to_code(node[3], prefix + "0"))
    return code

def build_huffman_tree(text, keylength=1):
    """Builds a binary tree representing the letter frequency of the text"""
    charcount = {}
    
    pos = 0    
    while pos < len(text):
        key = text[pos:pos + keylength]
        charcount[key] = charcount.setdefault(key, 0) + 1
        pos += keylength
    
    prioq = Queue.PriorityQueue()
    for item in charcount.iteritems():
        prioq.put_nowait((item[1], item[0], None, None)) 
    
    while prioq.qsize() > 1:
        left = prioq.get_nowait()
        right = prioq.get_nowait()
        internal_node = (left[0] + right[0], "", left, right)
        prioq.put_nowait(internal_node)
        
    return prioq.get_nowait()

def get_huffman_code(text):
    """Returns a Code-Dictionary { key=Character, value=Code }"""
    tree = build_huffman_tree(text)
    return convert_huffman_tree_to_code(tree)

def encrypt_text(text, code):
    """Encrypts a text with huffman-code"""
    crypted = []
    pos = 0
    keylength = len(code.keys()[0])
    while pos < len(text):
        key = text[pos:pos + keylength]
        crypted.append(code[key])
        pos += keylength
    
    return "".join(crypted) 

def decrypt_text(text, code):
    """Decrypts a text with huffman-code"""
    decrypted = []
    pos = 0
    while pos < len(text):
        for key, value in code.iteritems():
            if text[pos:].startswith(value):
                decrypted.append(key)
                pos += len(value)
                break
        else:
            raise KeyError
    return "".join(decrypted)

def main(text):
    """Shows sample usage of the functions for the Huffman-code."""
    print text
    code = get_huffman_code(text)
    
    # print code
    for key, value in sorted(code.iteritems(), key=lambda (k, v): (len(k), k)):
        print "%s: %s" % (key, value)

    crypted_text = encrypt_text(text, code)
    decrypted_text = decrypt_text(crypted_text, code)
    assert decrypted_text == text
    
    print crypted_text
    
    code_text = ""
    for key, value in code.iteritems():
        code_text += (key * 8) + ":" + value + "\n"
        
    result = (len(code_text),
              len(text) * 8, len(crypted_text),
              len(crypted_text) / (len(text) * 8.0) * 100,
              len(crypted_text + code_text) / (len(text) * 8.0) * 100)
    print "Code Length: %d, Text Length: %d, Crypted Text Length: %d - Percentage: %.1f %% / %.1f %% with Code" % result

if __name__ == "__main__":
    TEXT = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et 
dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd 
gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing 
elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos 
et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."""
    main(TEXT)
