__author__ = 'ICT-LXB'

import args

def main():
    import sys
    from args import Args
    from core import Core
    sys.exit(Core(Args().get_args()).obfuscate())