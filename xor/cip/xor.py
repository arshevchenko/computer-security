from itertools import izip, cycle
import base64

class XOR(object):
    def __init__(self, key):
        self.cipher_key = key

    def reset_key(self, key):
        self.cipher_key = key

    def decode_string(self, text):
        return self.xor(base64.decodestring(text))

    def encode_string(self, text):
        return base64.encodestring(self.xor(text)).strip()

    def xor(self, text):
        return "".join([chr(ord(a) ^ ord(b)) for a, b in izip(text, cycle(self.cipher_key))])
