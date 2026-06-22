def getInstruction(opcode):
    if opcode == "00000001100100":
        return "clrwdt"
    if opcode == "00000000001001":
        return "retfie"
    if opcode == "00000000001000":
        return "return"
    if opcode == "00000001100011":
        return "sleep"
    code = "Error"
    if opcode[0] == "0":
        if opcode[1] == "0":
            definingByte = opcode[2:6]
            if definingByte == "0000":
                #movwf or nop
                if opcode[6] == "0":
                    return "nop"
                else:
                    return f"movwf 0{hex(int(f'0b{opcode[7:]}',2)).lstrip('0x').upper()}h"
            if definingByte == "0001":
                if opcode[6] == "0":
                    return "clrw"
                else:
                    return f"clrf 0{hex(int(f'0b{opcode[7:]}',2)).lstrip('0x').upper()}h"
            #byte oriented file register operations
            byteOrientedFile = {"0111":"addwf",
                                "0101":"andwf",
                                "1001":"comf",
                                "0011":"decf",
                                "1011":"decfsz",
                                "1010":"incf",
                                "1111":"incfsz",
                                "0100":"iorwf",
                                "1000":"movf",
                                "1101":"rlf",
                                "1100":"rrf",
                                "0010":"subwf",
                                "1110":"swapf",
                                "0110":"xorwf"}
            code = byteOrientedFile[definingByte]
            return f"{code} 0{hex(int(f'0b{opcode[-7:]}',2)).lstrip('0x').upper()}h, {'w' if opcode[6]=='0' else 'f'}"
        else:
            if opcode[2:4] == "00":
                code = "bcf"
            elif opcode[2:4] == "01":
                code = "bsf"
            elif opcode[2:4] == "10":
                code = "btfsc"
            else:
                code = "btfss"
            return f"{code} 0{hex(int(f'0b{opcode[7:]}',2)).lstrip('0x').upper()}h, {int(f'0b{opcode[4:7]}',2)}"
            #bit oriented file register operations
    else: #1x xxxx xxxx xxxx
        if opcode[1:3] == "00":
            return f"call 0{hex(int(f'0b{opcode[3:]}',2)).lstrip('0x').upper()}h"
        elif opcode[1:3] == "01":
            return f"goto 0{hex(int(f'0b{opcode[3:]}',2)).lstrip('0x').upper()}h"
        else:
            definingByte = opcode[2:6]
            if definingByte[:-1] == "111":
                code = "addlw"
            elif definingByte == "1001":
                code = "andlw"
            elif definingByte == "1000":
                code = "iorlw"
            elif definingByte[:2] == "00":
                code = "movlw"
            elif definingByte[:2] == "01":
                code = "retlw"
            elif definingByte[:-1] == "110":
                code = "sublw"
            elif definingByte == "1010":
                code = "xorlw"
            return f"{code} 0{hex(int(f'0b{opcode[-8:]}',2)).lstrip('0x').upper()}h"
            #literal and control operations

def disasm(file):
    output = []
    with open(file, "r") as f:
        lines = f.readlines()
    for i in lines[1:]:
        for a in range(0,8):
            opcode = i[9+4*a:13+4*a]
            opcode = f"{str(opcode)[2:]}{str(opcode)[0:2]}"
            opcode = str(bin(int(opcode,16))).lstrip("0b").zfill(14)
            inst = getInstruction(opcode)
            output.append(inst)
    outputLines = "\n".join(output)
    with open("dissasm.asm", "w") as f:
        f.writelines(outputLines)
    return
    
    
