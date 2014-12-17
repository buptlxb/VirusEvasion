__author__ = 'ICT-LXB'

import pefile


class Core():
    def __init__(self, options):
        self.__options = options
        self.__binary = pefile.PE(self.__options.binary)

    def __checks_before_manipulations(self):
        return self.__binary is not None

    def obfuscate(self):
        if not self.__checks_before_manipulations():
            return False
        if self.__options.entry and not self.__obfuscate_entry():
            return False
        if self.__options.data and not self.__obfuscate_data():
            return False
        return True

    def __obfuscate_entry(self):
        print "[Error] {0}.{1}.__obfuscate_entry has not implemented".format(
            self.__module__, self.__class__.__name__)
        return False

    def __obfuscate_data(self):
        print "[Error] {0}.{1}.__obfuscate_data has not implemented".format(
            self.__module__, self.__class__.__name__)
        return False