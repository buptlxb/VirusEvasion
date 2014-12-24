import struct
import pype32


class XOR:
    """
decode:
    cld                       FC
    call get_pc               E8 1A 00 00 00
    add esi, 0fd9h            81 C6 D9 0F 00 00
    mov edi, esi              8B FE
    mov ecx, count            B9 78 56 34 12
decode@2:
    lodsb                     AC
    xor ax, 0ffh              34 FF
    stosb                     AA
    dec ecx                   49
    je target                 0F 84 06 00 01 00
    jmp decode@2              EB F3
get_pc proc
    mov esi, [esp]            8B 34 24
    ret                       C3
endp get_pc
    """

    def __init__(self, salt):
        self.salt = salt

    def encryptor(self, x):
        return x ^ self.salt

    def decryptor(self, rva, target, data_rva, data_size):
        decode_func = '\xFC\xE8\x1A\x00\x00\x00\x81\xC6'\
            + struct.pack('<l', data_rva - rva - 6) + '\x8B\xFE\xB9'\
            + struct.pack('<L', data_size) + '\xAC\x34' + struct.pack('<B', self.salt) + '\xAA\x49\x0F\x84'\
            + struct.pack('<l', target - rva - 30) + '\xEB\xF3\x8B\x34\x24\xC3'
        return decode_func

    def relocator(self, binary, rva, data_rva):
        binary.set_data_at_rva(rva+8, str(pype32.datatypes.DWORD(data_rva-rva-6)))