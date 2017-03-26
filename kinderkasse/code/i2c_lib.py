#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) Stephane Guerreau, GPL-Lizenz 
# Blog-Beitrag: http://hardware-libre.fr/2014/03/en-raspberry-pi-using-a-4x20-characters-display/
# und dem verknüpften GitHub Repository: https://github.com/CaptainStouf/raspberry_lcd4x20_I2C

import sys
import smbus
from time import *

class i2c_device:
    def __init__(self, addr, port=1):
        self.addr = addr
        self.bus = smbus.SMBus(port)

    # Write a single command
    def write_cmd(self, cmd):
        self.bus.write_byte(self.addr, cmd)
        sleep(0.0001)

    # Write a command and argument
    def write_cmd_arg(self, cmd, data):
        self.bus.write_byte_data(self.addr, cmd, data)
        sleep(0.0001)

    # Write a block of data
    def write_block_data(self, cmd, data):
        self.bus.write_block_data(self.addr, cmd, data)
        sleep(0.0001)

    # Read a single byte
    def read(self):
        return self.bus.read_byte(self.addr)

    # Read
    def read_data(self, cmd):
        return self.bus.read_byte_data(self.addr, cmd)

    # Read a block of data
    def read_block_data(self, cmd):
        return self.bus.read_block_data(self.addr, cmd)