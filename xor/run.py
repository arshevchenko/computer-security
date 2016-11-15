#!/usr/bin/python
from cip.xor import XOR

key = XOR("reference")
print key.encode_string("Hello")
print key.decode_string("OgAKCR0=")
