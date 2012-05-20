
def main(text, keylength):
    charcount = {}
    
    pos = 0    
    while pos < len(text):
        key = text[pos:pos+keylength]
        charcount[key] = charcount.setdefault(key, 0) + 1
        pos += keylength
    
    q = []
    for item in charcount.iteritems():
        q.append((item[1], item[0], None, None)) 
    
    while len(q) > 1:
        sq = sorted(q)
        n1, n2, q = sq[0], sq[1], sq[2:]
        internalNode = (n1[0]+n2[0], "", n1, n2)
        q.append(internalNode)
        
    root = q[0]
    
    def getCode(node, prefix=""):
        code = {}
        if node:
            if len(node[1]) > 0:
                code[node[1]] = prefix
            if node[2]:
                code.update(getCode(node[2], prefix+"1"))
            if node[3]:
                code.update(getCode(node[3], prefix+"0"))
        return code
    
    code = getCode(root)
    
    crypted = []
    pos = 0
    while pos < len(text):
        key = text[pos:pos+keylength]
        crypted.append(code[key])
        pos += keylength
    
    cryptedText = "".join(crypted) 
    
    decrypted = []
    pos = 0
    while pos < len(cryptedText):
        for key, value in code.iteritems():
            if cryptedText[pos:].startswith(value):
                decrypted.append(key)
                pos += len(value)
                break
        else:
            raise KeyError
        
    assert "".join(decrypted) == text
    
    codeText = ""
    for key, value in code.iteritems():
        codeText += (key*8) + value + "\n"

    return (keylength, len(codeText), len(text) * 8, len(cryptedText), len(cryptedText)/(len(text) * 0.08), len(cryptedText+codeText)/(len(text)*0.08)) 

import urllib2
text = urllib2.urlopen("https://bis.htu.tugraz.at").read()
#text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."

results = []
for x in range(1, 2):
    result = main(text, x)
    results.append(result)
    #print "Keylen: %d, Code: %d, Text: %d, Result: %d - Percentage: %.1f %% / %.1f %%" % result

for result in sorted(results, key=lambda x: x[-1]):
    print "Keylen: %d, Code: %d, Text: %d, Result: %d - Percentage: %.1f %% / %.1f %%" % result




