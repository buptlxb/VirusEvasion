import pype32
import junkcode


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
        # get the offset which junk code is to be writen to
        jc_offset = self.__binary.sectionHeaders[index].sizeOfRawData.value + self.__binary.sectionHeaders[
            index].pointerToRawData.value
        # get the relative virtual address of junk code
        jc_rva = self.__binary.getRvaFromOffset(jc_offset)
        # generate junk code
        jc = junkcode.generate(jc_rva, entry)
        # TODO bugs to fix
        # extend code section and insert payload
        self.__binary.extendSection(index, jc)
        # modify the entry point
        self.__binary.ntHeaders.optionalHeader.addressOfEntryPoint.value = jc_rva
        print '\t[*] PE entry obfuscation completed.'
        return True

    def __obfuscate_data(self):
        print "[Error] {0}.{1}.__obfuscate_data has not implemented".format(
            self.__module__, self.__class__.__name__)
        return False