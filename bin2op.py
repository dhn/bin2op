#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Extract the opcode from the objdump of a binary
'''

import os
import sys
import getopt
import string
from subprocess import check_output

__version__ = "$Id: bin2op.py,v 1.0 2015/12/27 15:47:42 dhn Exp $"
__license__ = "BSD"


def getopts():
    try:
        usage = ["file=", "short", "large", "intel", "att", "version", "help"]
        opts, args = getopt.getopt(sys.argv[1:], "f:sliavh", usage)

    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    objfile = None
    shellcode = None
    code = None
    syntax = "intel"
    for opt, arg in opts:
        if opt in ("-i", "--intel"):
            syntax = "intel"
        elif opt in ("-a", "--att"):
            syntax = "att"
        elif opt in ("-f", "--file"):
            objfile = arg
            if os.path.exists(objfile):
                shellcode, code = parse(objfile, syntax)
            else:
                print("[!] file does not exist")
                sys.exit(1)
        elif opt in ("-s", "--short"):
            if objfile is not None:
                print(shellcode)
        elif opt in ("-l", "--large"):
            if objfile is not None:
                for line in code:
                    print("", line)
        elif opt in ("-h", "--help"):
            usage()
        elif opt in ("-v", "--version"):
            print("%s - %s" % (__version__, __license__))
        else:
            assert False, "unhandled option"


def usage():
    print("usage: %s [options]" % __file__)
    print("   -f, --file     The assembly code filename")
    print("   -s, --short    Show less version of opcode")
    print("   -l, --large    Show verbose version of opcode")
    print("   -i, --intel    Use the intel assembly syntax")
    print("   -a, --att      Use the AT&T assembly syntax")
    print("")
    print("Example: %s -a -f bindshell/build/bindshell.o -l" % __file__)
    print("         %s -f bindshell/build/bindshell.o -s" % __file__)


# thanks zerosum0x0
def parse(obj, syntax):
    objdump = ['objdump', '-d', '-M', syntax, obj]

    lines = check_output(objdump)
    lines = lines.split(b'Disassembly of section')[1]
    lines = lines.split(b'\n')[3:]

    shellcode = ""
    code = []

    for line in lines:
        line = line.strip()

        tabs = line.split(b'\t')
        if (len(tabs) < 2):
            continue
        bytes = tabs[1].strip()

        instruction = "."
        if (len(tabs) == 3):
            instruction = tabs[2].strip().decode("utf-8")

        bytes = bytes.split(b' ')
        shellcodeline = ""
        for byte in bytes:
            shellcodeline += "\\x" + byte.decode("utf-8")

        shellcode += shellcodeline
        c = '%-*s/* %s */' % (32, '"'+shellcodeline+'"', instruction)
        code.append(c)

    return shellcode, code


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        usage()
    else:
        getopts()
