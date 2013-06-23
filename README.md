pyHuffman
=========

A module for illustrating the encode/decode of text with Huffman-Coding.

**Currently not intended to be used in real projects.** Due to my lack of knowledge of binary processing in python at 
that time, I implemented the "binary" processing just by handling Strings of the character "1" and "0" (very ugly and complicated!!).
Thats also the reason why I used the string-length as bit-count of the output code (to compare the size with the input).


This was one of my first python programms, so many things are not as pythonic as they could be.


### TODO:
* Use REAL binary code, not just strings with '0' and '1'.
* Performance Optimizations: Currently the conversion is very slow (probaby due to string-processing).

---

Sample:

    Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et 
    dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet 
    clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, 
    consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, 
    sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea 
    takimata sanctus est Lorem ipsum dolor sit amet.

Code:

     : 000
    e: 110
    t: 0010
    a: 0100
    o: 0101
    s: 0111
    r: 1000
    m: 1001
    u: 1011
    i: 1110
    d: 1111
    n: 01100
    l: 01101
    c: 001101
    p: 001111
    g: 101000
    ,: 101001
    v: 0011001
    b: 0011100
    .: 0011101
    y: 1010100
    k: 1010101
    L: 1010110
    \n: 1010111
    q: 001100000
    j: 001100001
    S: 001100010
    A: 001100011

Encrypted Text (just the first few Bits):

    101011001011000110100100011100011110111101110010001111010101101010110000000
    111111000100000100100111000101010010000011010101011000111110001011000101011
    100000001110100111111100011110111001101111001100101000000110011011110001010
    001010010000111110111100011111110010010010000110001010110010111001101010000
    011011101000100101011111000001011010010011110101100000011100110000110011110
    111110110110000100001011001000001101010000111000101100011000011000100001010
    111111101010110101011000110000100101001010000110001000000100011011110001100
    000101110101000100100100011010000100001010100100001111101111000111111100100
    100100000110010101011011011001111001010110100001110100000110001100100000011
    001110100001010001100101011100011000100000100001101001101101101110100100100
    011000100000011000011011011100100101000111110110101000111101010110101011000
    110011100011000100001100100000100011000111001011100100111010000011000100010
    ...
 
Code Length: 441, Text Length: 4760, Crypted Text Length: 2481 - Percentage: 52.1 % / 61.4 % with Code
