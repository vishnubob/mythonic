#!/usr/bin/env python

import os
import sys
import struct

FORMAT = "cH"
EEPROM_SIZE = 1024
FUSES = "-U lfuse:w:0xff:m -U hfuse:w:0xff:m -U efuse:w:0x07:m"

def write_eeprom(board_addr):
    board_addr = int(sys.agrv[1])
    threshold = 500
    image = struct.pack(FORAT, board_addr, threshold)
    rem = EEPROM_SIZE - len(image)
    image = image + (chr(0xFF) * rem)
    fn = "eeprom_board%s.txt" % board_addr

def write_board(port, board_addr):
    fuses_cmd = "avrdude -c avrispv2 -p m328 -P %s %s" % (port, FUSES)
    os.system(fuses_cmd)
    upload_cmd = "avrdude -c avrispv2 -p m328 -P %s -e -U flash:w:biscuit.hex" % port
    os.system(upload_cmd)
    eeprom_cmd = "avrdude -c avrispv2 -p m328 -P %s -e -U flash:w:eeprom_board%s.txt" % (port, board_addr)
    os.system(eeprom_cmd)

if __name__ == "__main__":
    port = sys.argv[1]
    board_cnt = int(sys.argv[2])
    if ':' in board_cnt:
        low, high = map(int, board_cnt(':'))
    else:
        low = int(board_cnt)
        high = low + 1
    for board_addr in range(low, high):
        print "Prepare board %s and hit enter." % board_addr
        write_eeprom(board_addr)
        write_board(port, board_addr)
