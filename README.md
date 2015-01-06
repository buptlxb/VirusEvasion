VirusEvasion
============

Virus Evasion is a virus obfuscation tool.

Usage
----

        usage: args.py [-h] [-e [ENTRY]] [-j {Simple,Jmp}] [-d] -b <binary> -o
                       <output> [--version]
        
        description:
          VirusEvasion provides evasion for your virus.
        
        optional arguments:
          -h, --help            show this help message and exit
          -e [ENTRY], --entry [ENTRY]
                                Obfuscate binary entry with [ENTRY_SIZE] code, default
                                size is 100
          -j {Simple,Jmp}, --junk {Simple,Jmp}
                                Specify the kind of Junk-code used in entry-
                                obfuscation, default choice is Simple
          -d, --data            Obfuscate binary .data section
          -b <binary>, --binary <binary>
                                Specify a binary filename to obfuscate
          -o <output>, --output <output>
                                Specify the output file name
          --version             Show program's version number and exit
        
        examples:
          VirusEvasion.py -e 500 --binary ./virus.exe --output ./output.exe
          VirusEvasion.py -e 500 -j Jmp --binary ./virus.exe --output ./output.exe
          VirusEvasion.py -d --binary ./virus.exe --output ./output.exe
          VirusEvasion.py -e 1024 -d -j --binary ./virus.exe --output ./output.exe


License
----

Copyright (c) 2014 WCG WZJ LXB <liuxuebao@gmail.com>. All rights reserved.