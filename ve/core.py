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
        # get the relative virtual address of junk code
        jc_rva = self.__binary.sectionHeaders[index].sizeOfRawData.value + self.__binary.sectionHeaders[
            index].virtualAddress.value
        # generate junk code
        jc = junkcode.generate(jc_rva, entry, 1 << 12)
        # TODO bugs to fix (sizeOfCode need to be adjusted)
        # extend code section and insert payload
        self.__binary.extendSection(index + 1, jc)
        # modify the entry point
        self.__binary.ntHeaders.optionalHeader.addressOfEntryPoint.value = jc_rva
        print '\t[*] PE entry obfuscation completed.'
        # import pype32.consts
        # import_dir = self.__binary.ntHeaders.optionalHeader.dataDirectory[pype32.consts.IMPORT_DIRECTORY]
        # for ide in import_dir.info:
        #     print hex(ide.originalFirstThunk.value),
        #     print hex(ide.timeDateStamp.value),
        #     print hex(ide.forwarderChain.value),
        #     print hex(ide.name.value),
        #     print hex(ide.firstThunk.value)
        #     for iate in ide.iat:
        #         print '\t', hex(iate.originalFirstThunk.value),
        #         print hex(iate.firstThunk.value),
        #         print iate.hint.value,
        #         print iate.name.value
        return True

    def __obfuscate_data(self):
        print "[Error] {0}.{1}.__obfuscate_data has not implemented".format(
            self.__module__, self.__class__.__name__)
        return False