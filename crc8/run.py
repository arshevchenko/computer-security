#!/usr/bin/python
from crc8.crc8 import CRC8
import sys

test_file = CRC8(sys.argv[1])
print "Result of CRC8 run: %s" % (test_file.getSum())
