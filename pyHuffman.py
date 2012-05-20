#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module for encoding/decoding Data with the Huffman-Coding"""

import Queue

__author__ = "Michael Krisper"
__email__ = "michael.krisper@htu.tugraz.at"
__date__ = "2012-05-20"

def convertHuffmanTreeToCode(node, prefix=""):
    code = {}    
    if node:
        if len(node[1]) > 0:
            code[node[1]] = prefix
        if node[2]:
            code.update(convertHuffmanTreeToCode(node[2], prefix + "1"))
        if node[3]:
            code.update(convertHuffmanTreeToCode(node[3], prefix + "0"))
    return code

def buildHuffmanTree(text, keylength=1):
    charcount = {}
    
    pos = 0    
    while pos < len(text):
        key = text[pos:pos + keylength]
        charcount[key] = charcount.setdefault(key, 0) + 1
        pos += keylength
    
    q = Queue.PriorityQueue()
    for item in charcount.iteritems():
        q.put_nowait((item[1], item[0], None, None)) 
    
    while q.qsize() > 1:
        n1 = q.get_nowait()
        n2 = q.get_nowait()
        internalNode = (n1[0] + n2[0], "", n1, n2)
        q.put_nowait(internalNode)
        
    root = q.get_nowait()
    return root

def getHuffmanCode(text):
    """Returns a Code-Dictionary { key=Letter, value=Huffman-Code } for the given Huffman-Tree"""
    tree = buildHuffmanTree(text)
    return convertHuffmanTreeToCode(tree)

def encryptText(text, code):
    crypted = []
    pos = 0
    keylength = len(code.keys()[0])
    while pos < len(text):
        key = text[pos:pos + keylength]
        crypted.append(code[key])
        pos += keylength
    
    cryptedText = "".join(crypted)
    return cryptedText 

def decryptText(text, code):
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
    print text
    code = getHuffmanCode(text)
    
    # print code
    for key, value in sorted(code.iteritems(), key=lambda x: (len(x[1]), x[1], x[0])):
        print "%s: %s" % (key, value)

    cryptedText = encryptText(text, code)
    decryptedText = decryptText(cryptedText, code)
    assert decryptedText == text
    
    print cryptedText
    
    codeText = ""
    for key, value in code.iteritems():
        codeText += (key * 8) + ":" + value + "\n"
        
    print "Code Length: %d, Text Length: %d, Crypted Text Length: %d - Percentage: %.1f %% / %.1f %% with Code" % \
        (len(codeText), len(text) * 8, len(cryptedText), len(cryptedText) / (len(text) * 0.08), len(cryptedText + codeText) / (len(text) * 0.08)) 

if __name__ == "__main__":
    text = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et 
dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd 
gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing 
elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos 
et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."""
    main(text)
