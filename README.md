# PIC16F886-Disassembler
A disassembler to convert from a HEX file read from a PIC16F886 to a moderatly readable .asm file


Program defines two functions, disasm and getInstruction

To use, call disasm with the file path as parameter. Eg - disasm("myHexFile.hex")
Writes the output to disasm.asm
