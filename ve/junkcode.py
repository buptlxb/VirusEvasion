import struct


def generate(rva, target):
    # jmp offset
    return '\xe9' + struct.pack('<l', target-rva-5)
