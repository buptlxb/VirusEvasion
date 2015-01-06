#!/usr/bin/env python
import argparse
import sys

from version import *


class Args:
    def __init__(self, arguments=None):
        self.__args = None
        if not arguments:
            arguments = sys.argv[1:]
        self.__parse(arguments)

    def __parse(self, arguments):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description="""description:
  VirusEvasion provides evasion for your virus.
""",
                                         epilog="""examples:
  VirusEvasion.py -e 500 --binary ./virus.exe --output ./output.exe
  VirusEvasion.py -e 500 -j Jmp --binary ./virus.exe --output ./output.exe
  VirusEvasion.py -d --binary ./virus.exe --output ./output.exe
  VirusEvasion.py -e 1024 -d -j --binary ./virus.exe --output ./output.exe

  """)

        parser.add_argument("-e", "--entry", type=int, nargs="?", const=100, help="Obfuscate binary entry with [ENTRY_SIZE] code, default size is 100")
        parser.add_argument("-j", "--junk", type=str, choices=['Simple', 'Jmp', 'Math'], default='Simple', help="Specify the kind of Junk-code used in entry-obfuscation, default choice is Simple")
        parser.add_argument("-d", "--data", action="store_true", help="Obfuscate binary .data section")
        parser.add_argument("-b", "--binary", type=str, metavar="<binary>", required=True, help="Specify a binary filename to obfuscate")
        parser.add_argument("-o", "--output", type=str, metavar="<output>", required=True, help="Specify the output file name")
        parser.add_argument("--version", action="version", version=PYVIRUSEVASION_VERSION, help="Show program's version number and exit")
        self.__args = parser.parse_args(arguments)
        print '[+] Parsing arguments completed.'

        if self.__args.entry is not None and self.__args.entry < 5:
            print 'Error: Obfuscate binary entry size ({0:d}) must not be less than 5'.format(self.__args.entry)
            sys.exit(0)

    def get_args(self):
        return self.__args

if __name__ == '__main__':
    print Args(['-h']).get_args()