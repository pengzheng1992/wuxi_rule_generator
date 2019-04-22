#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Keywords exclude 0x and 0X. 
# probability of fivetuple and keyword is bug-fixed.
# probability of '!' is 1/4
# probability of single keyword is 2/3
# length of keyword is 5 to MAXLEN.

import re
import random
#import string
from enum import Enum

MINLEN = 5
MAXLEN = 128

class Hex_mode(Enum):
    LETTER_DIGITS = 1
    ALL_CHARS = 2

HEX_MODE = Hex_mode.ALL_CHARS

#all chars
#def genRandomStringChar(slen = 3):
#    s = ""
#    n = slen
#    while n > 0:
#        rdi = random.randint(34, 126)
#        while rdi == 35 or rdi == 58 or rdi == 44:
#            rdi = random.randint(34, 126)
#        s = s + chr(rdi)
#        n = n - 1
#    return s

#only letters
#def genRandomStringChar2(slen = 3):
#    s = ""
#    n = slen
#    while n > 0:
#        s += random.choice(string.ascii_letters)
#        n = n - 1
#    return s

# letters and digits
def genRandomStringChar3(slen):
    assert slen >= 3, 'slen < 3'
    s = ""
    n = slen
    zeroX = False
    while n > 0:
        rdi = random.randint(48, 122) # '0' -- 'z'
        # punctuations excluded, '0x' or '0X' excluded.
        while (rdi >= 58 and rdi <= 64) or (rdi >= 91 and rdi <= 96) or (zeroX and (rdi == 88 or rdi == 120)):
            rdi = random.randint(48, 122)
        if rdi == 48: # rdi == '0'
            zeroX = True
        else:
            zeroX = False
        s = s + chr(rdi)
        n = n - 1
    return s

def genStringChar(slen):
    assert slen >= 3, 'slen < 3'
    return genRandomStringChar3(slen)

#all chars 0-255
def genStringHex1(slen = 3):
    assert slen >= 3, 'slen < 3'
    if slen <= 0:
        return ""
    s = "0"
    s = s + random.choice(('x', 'X'))
    rdi = random.randint(0, 255)
    if rdi >= 0 and rdi <= 15:
        s += '0'
    hrdi = hex(rdi)
    s = s + hrdi[2:]
    n = slen - 1
    while n > 0:
        s = s + ' '
        rdi = random.randint(0, 255)
        if rdi >= 0 and rdi <= 15:
            s += '0'
        hrdi = hex(rdi)
        s = s + hrdi[2:]
        n = n - 1
    return s

def genStringHex(slen):
    assert slen >= 3, 'slen < 3'
    if HEX_MODE == Hex_mode.ALL_CHARS:
        return genStringHex1(slen)
    elif HEX_MODE == Hex_mode.LETTER_DIGITS:
        return genStringHex2(slen)
    else:
        assert False, 'HEX_MODE error!'

#only letters and digits
def genStringHex2(slen):
    assert slen >= 3, 'slen < 3'
    if slen <= 0:
        return ""
    s = "0"
    s = s + random.choice(('x', 'X'))
    rdi = random.randint(48, 122)
    while (rdi >= 58 and rdi <= 64) or (rdi >= 91 and rdi <= 96):
        rdi = random.randint(48, 122)
    hrdi = hex(rdi)
    s = s + hrdi[2:]
    n = slen - 1
    while n > 0:
        s = s + ' '
        rdi = random.randint(48, 122)
        while (rdi >= 58 and rdi <= 64) or (rdi >= 91 and rdi <= 96):
            rdi = random.randint(48, 122)
        hrdi = hex(rdi)
        s = s + hrdi[2:]
        n = n - 1
    return s

def genStringCharHex(slen = 128):
    rdi = random.randint(6, slen)
    rdi2 = random.randint(3, rdi - 3)
    return genStringChar(rdi2) + genStringHex(rdi - rdi2)

def genStringHexChar(slen = 128):
    rdi = random.randint(6, slen)
    rdi2 = random.randint(3, rdi - 3)
    return genStringHex(rdi2) + genStringChar(rdi - rdi2)

def genStringCharHexChar(slen = 128):
    rdi1 = random.randint(3, slen // 3)
    rdi2 = random.randint(3, slen // 3)
    rdi3 = random.randint(3, slen // 3)
    return genStringChar(rdi1) + genStringHex(rdi2) + genStringChar(rdi3)

def genKeyword():
    s = random.choice((genStringChar(random.randint(MINLEN,MAXLEN)), genStringHex(random.randint(MINLEN,MAXLEN)), genStringCharHex(MAXLEN), genStringHexChar(MAXLEN), genStringCharHexChar(MAXLEN)))
    rdiPos = random.randint(0, 150);
    prefix = random.choice(("", str(rdiPos) + ':'))
    rdi = random.randint(0, 3) # probability of '!' is 1/4
    if rdi == 0:
        prefix += '!'
    s = prefix + s
    #s = random.choice(("", str(rdiPos) + ':')) + random.choice(("", '!')) + s
    return s

def genKeywordRule():
    keywordrule = '#'
    s = genKeyword()
    keywordrule += s
    m = random.randint(-3, 2) # 2/3 probability single keyword, 1/6 probability 2 keywords, 1/6 probability 3 keywords.
    i = 0
    while i < m:
        keywordrule += ','
        s = genKeyword()
        keywordrule += s
        i = i + 1
    return keywordrule

def main():
    reg = re.compile('^@(?P<sip>[^/]*)/(?P<smask>[^\s]*)\s(?P<dip>[^/]*)/(?P<dmask>[^\s]*)\s(?P<sport>[^\s]*) : (?P<sport2>[^\s]*)\s(?P<dport>[^\s]*) : (?P<dport2>[^\s]*)\s(?P<proto>[^/]*)/')
    with open('MyFilter60000', 'r') as inputFile, open('hybridX-allchars-128.txt', 'w') as outputFile:
        for line in inputFile:
            outputFile.write(random.choice(('IPFF', 'LINK')) + '^')
            rdi = random.randint(0, 2)
            #rdi = 0
            # MAXDICE = 20 means probability of '*' is 5%
            MAXDICE = 20
            #tuple-5 rule
            if rdi == 0 or rdi == 1:
                regMatch = reg.match(line)
                linebits = regMatch.groupdict()
    
                protocol = int(linebits['proto'], 16)
    #            outputFile.write(random.choice((str(protocol), '*')) + '@')
                dice = random.randint(1, MAXDICE)
                if dice == 1:
                    outputFile.write('*')
                else:
                    outputFile.write(str(protocol))
                outputFile.write('@')
    
                smask = linebits['smask']
                n = int(smask)
                addr = 0xffffffff << (32-n)
                addrmask = "%u.%u.%u.%u" % ((addr >> 24) & 0xff, (addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff)
    #            outputFile.write(random.choice(('*', linebits['sip'] + random.choice(('', '/' + addrmask)))))
                dice = random.randint(1, MAXDICE)
                if dice == 1:
                    outputFile.write('*')
                else:
                    outputFile.write(linebits['sip'] + random.choice(('', '/' + addrmask)))
    
                outputFile.write(':')
    #            outputFile.write(random.choice(('*', linebits['sport'])))
                dice = random.randint(1, MAXDICE)
                if dice == 1:
                    outputFile.write('*')
                else:
                    outputFile.write(linebits['sport'])
    
                outputFile.write(random.choice(('<', '>', '<>')))
    
                dmask = linebits['dmask']
                n = int(dmask)
                addr = 0xffffffff << (32-n)
                addrmask = "%u.%u.%u.%u" % ((addr >> 24) & 0xff, (addr >> 16) & 0xff, (addr >> 8) & 0xff, addr & 0xff)
    #            outputFile.write(random.choice(('*', linebits['dip'] + random.choice(('', '/' + addrmask)))))
                dice = random.randint(1, MAXDICE)
                if dice == 1:
                    outputFile.write('*')
                else:
                    outputFile.write(linebits['dip'] + random.choice(('', '/' + addrmask)))
    
                outputFile.write(':')
    #            outputFile.write(random.choice(('*', linebits['dport'])))
                dice = random.randint(1, MAXDICE)
                if dice == 1:
                    outputFile.write('*')
                else:
                    outputFile.write(linebits['dport'])
    
            # keyword rule
            if rdi == 1 or rdi == 2:
                keywordrule = genKeywordRule()
                outputFile.write(keywordrule)
    
            outputFile.write('\n')

if __name__ == '__main__':
    main()
