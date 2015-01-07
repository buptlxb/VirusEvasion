#!/usr/bin/env python
import pype32
import junkcode
import translator


class Core():
    def __init__(self, options):
        self.__options = options
        self.__binary = pype32.PE(self.__options.binary)
        print '[+] Parsing PE file completed.'

    def __checks_before_manipulations(self):
        return self.__binary is not None

    def obfuscate(self):
        print '[+] Obfuscation start:'
        if not self.__checks_before_manipulations():
            return False
        if self.__options.entry >= 5 and not self.__obfuscate_entry(self.__options.junk):
            return False
        if self.__options.data and not self.__obfuscate_data():
            return False
        print '[+] Obfuscation completed.'
        # self.__binary.extendSection(3, '\xff')
        self.__binary.write(self.__options.output)
        print '[+] Writing new PE completed.'

        return True

    def __obfuscate_entry(self, junk_prefix):
        # get entry point virtual address
        entry = self.__binary.ntHeaders.optionalHeader.addressOfEntryPoint.value
        # get index of the section which entry resides
        index = self.__binary.getSectionByRva(entry)
        # get the relative virtual address of junk code
        jc_rva = self.__binary.sectionHeaders[index].misc.value + self.__binary.sectionHeaders[
            index].virtualAddress.value
        # generate junk code
        junk_name = junk_prefix + 'Junk'
        junk_class = getattr(junkcode, junk_name)
        assert callable(junk_class), '{0}.{1} is not callable!'.format(junk_name, junk_class)
        jc = junk_class(jc_rva, entry, self.__options.entry).generate()
        # extend code section and insert payload
        self.__binary.extendSection(index + 1, jc)
        # modify the entry point
        self.__binary.ntHeaders.optionalHeader.addressOfEntryPoint.value = jc_rva
        print '\t[*] PE entry(0x{0:x}) obfuscation completed.'.format(self.__options.entry)
        return True

    def __obfuscate_data(self):
        # get entry point virtual address
        optional_header = self.__binary.ntHeaders.optionalHeader
        # set the encrypt salt
        salt = 0xFF
        # get the XOR translator
        xor = translator.XORPlus(salt)
        # encrypt the data section
        df_rva, data_size = self.__binary.encrypt_data_section(xor)
        # modify the entry point
        if df_rva:
            optional_header.addressOfEntryPoint.value = df_rva
        print '\t[*] PE data(0x{0:x}) obfuscation completed.'.format(data_size)
        return True