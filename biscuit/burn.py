#!/usr/bin/env python

import os
import sys
import struct

FORMAT = "BH"
EEPROM_SIZE = 1024
FUSES = ["-U lfuse:w:0xff:m", "-U hfuse:w:0xd9:m", "-U efuse:w:0x07:m"]

def write_eeprom(board_addr):
    threshold = 500
    image = struct.pack(FORMAT, board_addr, threshold)
    rem = EEPROM_SIZE - len(image)
    image = image + (chr(0xFF) * rem)
    #image = str.join(',', ["0x%02x" % ord(val) for val in image]) + '\n'
    fn = "eeprom_board%s.txt" % (board_addr + 1)
    f = open(fn, 'w')
    f.write(image)

def write_board(port, board_addr):
    for fuse in FUSES:
        fuses_cmd = "avrdude -c avrispv2 -p m328p -F -P %s %s" % (port, fuse)
        print fuses_cmd
        ret = os.system(fuses_cmd)
        assert(ret == 0)
    upload_cmd = "avrdude -c avrispv2 -p m328p -F -P %s -e -U flash:w:biscuit.hex" % port
    print upload_cmd
    ret = os.system(upload_cmd)
    assert(ret == 0)
    eeprom_cmd = "avrdude -c avrispv2 -p m328p -F -P %s -U eeprom:w:eeprom_board%s.txt" % (port, board_addr + 1)
    print eeprom_cmd
    ret = os.system(eeprom_cmd)
    assert(ret == 0)

if __name__ == "__main__":
    port = sys.argv[1]
    board_cnt = sys.argv[2]
    if ':' in board_cnt:
        low, high = map(int, board_cnt.split(':'))
    else:
        low = int(board_cnt)
        high = low + 1
    low = low - 1
    high = high - 1
    for board_addr in range(low, high):
        msg = "Prepare board %s and hit enter." % (board_addr + 1)
        raw_input(msg)
        write_eeprom(board_addr)
        write_board(port, board_addr)
