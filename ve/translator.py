import struct
import pype32


class XORPlus:
    """
decrypt:
    mov esi, 12345678h      BE 78 56 34 12
    mov edx, 12345678h      BA 78 56 34 12
again:
    lodsd                   AD
    mov edi, eax            8B F8
    lodsd                   AD
    mov ecx, eax            8B C8
    call decode             E8 09 00 00 00
    dec edx                 4A
    je target               0F 84 11 00 01 00
    jmp again               EB EC

decode proc
    push esi                56
    push edi                57
    cld                     FC
    mov esi, edi            8B F7
decode@1:
    lodsb                   AC
    xor al, 0ffh            34 FF
    stosb                   AA
    dec ecx                 49
    jne decode@1            75 F9
    pop edi                 5F
    pop esi                 5E
    ret                     C3
endp decode
    """
    def __init__(self, salt):
        self.salt = salt

    def encryptor(self, x):
        return x ^ self.salt

    def decryptor(self, rva, target, data_va, data_size):
        decode_func = '\xBE' + struct.pack('<L', data_va) + \
                      '\xBA' + struct.pack('<L', data_size >> 3) + \
                      '\xAD\x8B\xF8\xAD\x8B\xC8\xE8\x09\x00\x00\x00\x4A\x0F\x84' + struct.pack("<l", target-rva-28) + \
                      '\xEB\xEC\x56\x57\xFC\x8B\xF7\xAC\x34' + struct.pack('<B', self.salt) + \
                      '\xAA\x49\x75\xF9\x5F\x5E\xC3'
        return decode_func

    def relocator(self, binary, rva, data_va):
        binary.set_data_at_rva(rva+1, struct.pack('<L', data_va))
        binary.add_relocation([rva+1])