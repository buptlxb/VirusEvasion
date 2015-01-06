#!/usr/bin/env python
import struct


class BasicJunk:
    def __init__(self, rva, target, size):
        self.rva = rva
        self.target = target
        self.size = size

    def gengerate(self):
        assert False, self.__class__.__name__ + '.generate() must be overridden!.'


class SimpleJunk(BasicJunk):
    r"""
    >>> SimpleJunk(0x1000, 0x1010, 16).generate()
    '\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xe9\x00\x00\x00\x00'
    """
    def __init__(self, rva, target, size=5):
        self.rva = rva
        self.target = target
        self.size = size

    def generate(self):
        # jmp offset
        return '\x90' * (self.size - 5) + '\xe9' + struct.pack('<l', self.target - self.rva - self.size)


class JmpJunk(BasicJunk):
    r"""
    >>> JmpJunk(0x1000, 0x1010, 16).generate()
    '\xeb\x03\x90\x90\x90\xeb\x03\x90\x90\x90\x90\xe9\x00\x00\x00\x00'
    """
    def __init__(self, rva, target, size=5):
        self.rva = rva
        self.target = target
        self.size = size

    def generate(self):
        """
            jmp @1:
        @1:
            jmp @2:
        @2:
            ...
        """
        leading_size = self.size - 5
        assert leading_size >= 0, 'JmpJunk size should not be less than 5.'
        jmp = '\xeb\x03\x90\x90\x90'
        jmp_size = len(jmp)
        repeat = leading_size / jmp_size
        nops = leading_size % jmp_size
        return jmp * repeat + '\x90' * nops + '\xe9' + struct.pack('<l', self.target - self.rva - self.size)


class MathJunk(BasicJunk):
    r"""
    >>> MathJunk(0x1000, 0x1018, 24).generate()
    '3\xc0\xb9\x03\x00\x00\x00\x03\xc13\xc0\xb9\x03\x00\x00\x00\x03\xc1\x90\xe9\x00\x00\x00\x00'
    """
    def generate(self):
        """
        xor eax, eax        33 C0
        mov ecx, 3          B9 00 00 00 03
        add eax, edx        03 C1
        """
        leading_size = self.size - 5
        assert leading_size >= 0, 'JmpJunk size should not be less than 5.'
        math = '\x33\xC0\xB9\x03\x00\x00\x00\x03\xC1'
        math_size = len(math)
        repeat = leading_size / math_size
        nops = leading_size % math_size
        return math * repeat + '\x90' * nops + '\xe9' + struct.pack('<l', self.target - self.rva - self.size)

if __name__ == '__main__':
    import doctest
    doctest.testmod()