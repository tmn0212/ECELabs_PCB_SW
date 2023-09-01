# from readwriteIO import *
import readwriteIO
from setupIO import *

"""
    These functions are meant to replicate the current SW setup using gpiozero and pigpio library.
    They are aimed to make implementation onto the current setup easier.
    However, they haven't been fully tested (about 80% done) and verified the design. 
"""

# Function to replace LED(#).on() of Pi Zero (gpiozero)
class LED:
    def __init__(self, index):
        self.index = index

    def on(self):
        if 0 <= self.index <= 20:
            pin = self.index

            if 0 <= pin <= 7:
                pin = self.index
                mcp_addr = 0x20
                port_addr = 0x12
                
            
            elif 8 <= pin <= 15:
                pin = self.index - 8
                mcp_addr = 0x20
                port_addr = 0x13
                
            elif 16 <= pin <= 20:
                pin = self.index - 16
                mcp_addr = 0x21
                port_addr = 0x12

        readwriteIO.write_bit(mcp_addr, port_addr, pin, bit=1)

    def off(self):
        if 0 <= self.index <= 20:
            pin = self.index

            if 0 <= pin <= 7:
                pin = self.index
                mcp_addr = 0x20
                port_addr = 0x12
                
            
            elif 8 <= pin <= 15:
                pin = self.index - 8
                mcp_addr = 0x20
                port_addr = 0x13
                
            elif 16 <= pin <= 20:
                pin = self.index - 16
                mcp_addr = 0x21
                port_addr = 0x12

        readwriteIO.write_bit(mcp_addr, port_addr, pin, bit=0)


# Function to replace Pi4B (pigpio)
class pi:
    def read_bank_1(self):
        right_pins = format(readwriteIO.read_port(mcp_addr=0x26, port_addr=0x13), '08b')[::-1]
        left_pins = format(readwriteIO.read_port(mcp_addr=0x25, port_addr=0x12), '08b')[::-1]
        LED_pins = format(readwriteIO.read_port(mcp_addr=0x26, port_addr=0x12), '03b')[::-1]

        return int("".join([LED_pins, left_pins, right_pins]), 2)
    
    def stop(self):
        return
