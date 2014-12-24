VirusEvasion
============

Virus Evasion is a virus obfuscation tool.

Usage
----

    usage: VirusEvasion.py [-h] [-v] [-e [ENTRY]] [-d] -b <binary> -o <output>

    description:
      VirusEvasion provides evasion for your virus.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         Display the VirusEvasion's version
      -e [ENTRY], --entry [ENTRY]
                            Obfuscate binary entry with [ENTRY_SIZE] code, default
                            size is 100
      -d, --data            Obfuscate binary .data section
      -b <binary>, --binary <binary>
                            Specify a binary filename to obfuscate
      -o <output>, --output <output>
                            Specify the output file name

    examples:
      VirusEvasion.py -e -d --binary ./virus.exe --output ./output.exe

License
----

Copyright (c) 2014 WCG WZJ LXB <liuxuebao@gmail.com>. All rights reserved.