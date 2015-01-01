#!/usr/bin/env python
import struct


def generate(rva, target, size=5):
    # jmp offset
    return '\x90' * (size-5) + '\xe9' + struct.pack('<l', target-rva-size)
