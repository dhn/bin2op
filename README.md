# bin2op
Extract the opcode from the objdump of a binary

## Usage
```
usage: ./bin2op.py [options]
   -f, --file     The assembly code filename
   -s, --short    Show less version of opcode
   -l, --large    Show verbose version of opcode
   -i, --intel    Use the intel assembly syntax
   -a, --att      Use the AT&T assembly syntax

Example: ./bin2op.py -a -f bindshell/build/bindshell.o -l
         ./bin2op.py -f bindshell/build/bindshell.o -s
```
