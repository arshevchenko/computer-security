import binascii

class CRC8(object):

    def __init__(self, file_name):
        self.msg = ""
        self.check = 0
        with open(file_name, "rb") as file_cont:
            self.msg = bytearray(str(file_cont.read()).encode("hex"))

    def add_CRC(self, byte, crc):
        sec_byte = byte + 256 if byte < 0 else byte
        for i in xrange(8):
            odd = ((sec_byte ^ crc) & 1) == 1
            crc >>= 1
            sec_byte >>= 1
            if (odd):
                crc ^= 0x8C
        return crc

    def checkSum(self):
        for byte in self.msg:
            self.check = self.add_CRC(byte, self.check)

    def getSum(self):
        if self.check == 0:
            self.checkSum()
        return self.check
