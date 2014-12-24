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
        if self.__options.entry and not self.__obfuscate_entry():
            return False
        self.__binary.write(r"E:\cspace\output2.exe")
        if self.__options.data and not self.__obfuscate_data():
            return False
        print '[+] Obfuscation completed.'
        self.__binary.write(self.__options.output)
        print '[+] Writing new PE completed.'
        return True

    def __obfuscate_entry(self):
        # get entry point virtual address
        entry = self.__binary.ntHeaders.optionalHeader.addressOfEntryPoint.value
        # get index of the section which entry resides
        index = self.__binary.getSectionByRva(entry)
        # get the relative virtual address of junk code
        jc_rva = self.__binary.sectionHeaders[index].sizeOfRawData.value + self.__binary.sectionHeaders[
            index].virtualAddress.value
        # generate junk code
        jc = junkcode.generate(jc_rva, entry, 1 << 12)
        # extend code section and insert payload
        self.__binary.extendSection(index + 1, jc)
        # modify the entry point
        self.__binary.ntHeaders.optionalHeader.addressOfEntryPoint.value = jc_rva
        print '\t[*] PE entry obfuscation completed.'
        return True

    def __obfuscate_data(self):
        # get entry point virtual address
        optional_header = self.__binary.ntHeaders.optionalHeader
        # set the encrypt salt
        salt = 0xFF
        # get the XOR translator
        xor = translator.XOR(salt)
        # encrypt the data section
        df_rva, data_size = self.__binary.encrypt_data_section(xor)
        # modify the entry point
        optional_header.addressOfEntryPoint.value = df_rva
        print '\t[*] PE data(0x{0:x}) obfuscation completed.'.format(data_size)
        return True