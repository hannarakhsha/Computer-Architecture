#!/usr/bin/env python
import sys
import os

for i in range(len(sys.argv)):
    if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
        inputFileName = sys.argv[i + 1]
    elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
        outputFileName = sys.argv[i + 1]

specialMask = 0x1FFFFF

rnMask = 0x3E0 # 1st argument ARM Rn
rmMask = 0x1F0000 # 2nd argument ARM Rm
rdMask = 0x1F # Destination ARM Rd
imMask = 0x3FFC00 # ARM I Immediate
shmtMask = 0xFC00 # ARM Shamt
addrMask = 0x1FF000 # ARM Address for LD/ST
addrCBMask = 0xFFFFE0 # addr for CB format
imsftMask = 0x600000 # shift for IM format
imdataMask = 0x1FFFE0 # data for IM type

opcodeStr = []
validStr = []
instrSpaced = []
arg1 = []
arg2 = []
arg3 = []
arg1Str = []
arg2Str = []
arg3Str = []
mem = []
opcode = []
instructions = []
data = []
dataPrint = []
i = 0
memoryLocationDis = 96
memoryLocationData = 96
cycle = 1

class Disassembler:

    def run(self):
        global opcodeStr
        global validStr
        global arg1
        global arg2
        global arg3
        global arg1Str
        global arg2Str
        global arg3Str
        global mem
        global opcode
        global instructions
        global i
        global data
        global memoryLocationData

        global specialMask
        global rnMask
        global rmMask
        global rdMask
        global imMask
        global shmtMask
        global addrMask
        global addrCBMask
        global imsftMask
        global imdataMask

        opcode.append(binaryToDecimal(instructions[0:11]))

        def printBinaryandMemory(instructions):
            global memoryLocationDis
            global i

            instrSpaced.append(instructions[0:8] + ' ' + instructions[8:11] + ' ' + instructions[11:16] + ' ' +
                               instructions[16:21] + ' ' + instructions[21:26] + ' ' + instructions[26:32] + '\t')

            mem.append(str(memoryLocationDis) + '\t')
            outFileDis.write(str(instrSpaced[i]) + str(mem[i]))

            memoryLocationDis += 4

        printBinaryandMemory(instructions)

        if opcode[i] >= 160 and opcode[i] <= 191:
            opcodeStr.append('B')
            validStr.append('Y')

            if (instructions[6] == '0'):
                arg1.append((int(instructions, base=2) & specialMask))
                arg2.append((int(instructions, base=2) & specialMask))
                arg3.append((int(instructions, base=2) & specialMask))
                arg1Str.append('\t#' + str(arg3[i]) + '\n')
                arg2Str.append('\t#' + str(arg1[i]) + '\n')
                arg3Str.append('\t#' + str(arg2[i]) + '\n')

            elif (instructions[6] == '1'):
                address = instructions[6:32]
                value = twosComplement(int(address, 2), len(address))

                arg1.append(value)
                arg2.append(value)
                arg3.append(value)
                arg1Str.append('\t#' + str(arg3[i]) + '\n')
                arg2Str.append('\t#' + str(arg1[i]) + '\n')
                arg3Str.append('\t#' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + "   " + arg1Str[i])

        elif opcode[i] == 1104:
            opcodeStr.append('AND')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & rmMask) >> 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', R' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1112:
            opcodeStr.append('ADD')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & rmMask) >> 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', R' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] >= 1160 and opcode[i] <= 1161:
            opcodeStr.append('ADDI')
            validStr.append('Y')

            if (instructions[10] == '0'):
                arg1.append((int(instructions, base=2) & rnMask) >> 5)
                arg2.append((int(instructions, base=2) & imMask) >> 10)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]) + '\n')

            elif (instructions[10] == '1'):
                immediate = instructions[10:22]
                value = twosComplement(int(immediate, 2), len(immediate))

                arg1.append((int(instructions, base=2) & rnMask) >> 5)
                arg2.append(value)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1360:
            opcodeStr.append('ORR')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & rmMask) >> 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', R' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] >= 1440 and opcode[i] <= 1447:
            opcodeStr.append('CBZ')
            validStr.append('Y')

            if (instructions[8] == '0'):
                arg1.append((int(instructions, base=2) & addrCBMask) >> 5)
                arg2.append((int(instructions, base=2) & addrCBMask) >> 5)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', #' + str(arg1[i]) + '\n')
                arg3Str.append('' + str(arg2[i]) + '\n')

            elif (instructions[8] == '1'):
                address = instructions[8:27]
                value = twosComplement(int(address, 2), len(address))

                arg1.append(value)
                arg2.append(value)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', #' + str(arg1[i]) + '\n')
                arg3Str.append('' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i])

        elif opcode[i] >= 1448 and opcode[i] <= 1455:
            opcodeStr.append('CBNZ')
            validStr.append('Y')

            if (instructions[8] == '0'):
                arg1.append((int(instructions, base=2) & addrCBMask) >> 5)
                arg2.append((int(instructions, base=2) & addrCBMask) >> 5)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', #' + str(arg1[i]) + '\n')
                arg3Str.append('' + str(arg2[i]) + '\n')

            elif (instructions[8] == '1'):
                address = instructions[8:27]
                value = twosComplement(int(address, 2), len(address))

                arg1.append(value)
                arg2.append(value)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', #' + str(arg1[i]) + '\n')
                arg3Str.append('' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i])

        elif opcode[i] == 1624:
            opcodeStr.append('SUB')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & rmMask) >> 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', R' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] >= 1672 and opcode[i] <= 1673:
            opcodeStr.append('SUBI')
            validStr.append('Y')

            if (instructions[10] == '0'):
                arg1.append((int(instructions, base=2) & rnMask) >> 5)
                arg2.append((int(instructions, base=2) & imMask) >> 10)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]) + '\n')
            elif (instructions[10] == '1'):
                immediate = instructions[10:22]
                value = twosComplement(int(immediate, 2), len(immediate))

                arg1.append((int(instructions, base=2) & rnMask) >> 5)
                arg2.append(value)
                arg3.append((int(instructions, base=2) & rdMask) >> 0)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] >= 1684 and opcode[i] <= 1687:
            opcodeStr.append('MOVZ')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & imdataMask) >> 5)
            arg2.append(((int(instructions, base=2) & imsftMask) >> 21) * 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', ' + str(arg1[i]))
            arg3Str.append(', LSL ' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] >= 1940 and opcode[i] <= 1943:
            opcodeStr.append('MOVK')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & imdataMask) >> 5)
            arg2.append(((int(instructions, base=2) & imsftMask) >> 21) * 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', ' + str(arg1[i]))
            arg3Str.append(', LSL ' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1690:
            opcodeStr.append('LSR')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & shmtMask) >> 10)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', #' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1691:
            opcodeStr.append('LSL')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & shmtMask) >> 10)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', #' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1692:
            opcodeStr.append('ASR')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & shmtMask) >> 10)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', #' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1984:
            opcodeStr.append('STUR')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & addrMask) >> 12)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', [R' + str(arg1[i]))
            arg3Str.append(', #' + str(arg2[i]) + ']\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1986:
            opcodeStr.append('LDUR')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & addrMask) >> 12)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', [R' + str(arg1[i]))
            arg3Str.append(', #' + str(arg2[i]) + ']\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif opcode[i] == 1872:
            opcodeStr.append('EOR')
            validStr.append('Y')

            arg1.append((int(instructions, base=2) & rnMask) >> 5)
            arg2.append((int(instructions, base=2) & rmMask) >> 16)
            arg3.append((int(instructions, base=2) & rdMask) >> 0)
            arg1Str.append('\tR' + str(arg3[i]))
            arg2Str.append(', R' + str(arg1[i]))
            arg3Str.append(', R' + str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i] + " " + arg1Str[i] + arg2Str[i] + arg3Str[i])

        elif int(instructions,2) == 0:
            opcodeStr.append('NOP\n')
            validStr.append('Y')

            arg1.append('')
            arg2.append('')
            arg3.append('')
            arg1Str.append(str(arg3[i]))
            arg2Str.append(str(arg1[i]))
            arg3Str.append(str(arg2[i]))

            data.append(0)
            dataPrint.append(0)
            outFileDis.write(opcodeStr[i])

        elif opcode[i] == 2038:
            opcodeStr.append('BREAK')
            validStr.append('Y')

            arg1.append('')
            arg2.append('')
            arg3.append('')
            arg1Str.append(str(arg3[i]))
            arg2Str.append(str(arg1[i]))
            arg3Str.append(str(arg2[i]) + '\n')

            data.append(0)
            dataPrint.append(0)
            memoryLocationData = memoryLocationDis
            outFileDis.write(opcodeStr[i] + '\n')

        else:
            opcodeStr.append('Data\n')
            validStr.append('N')

            arg1.append('')
            arg2.append('')
            arg3.append('')
            arg1Str.append(str(arg3[i]))
            arg2Str.append(str(arg1[i]))
            arg3Str.append(str(arg2[i]))

            if int(instructions,2) >> 31 == 1:
                twosComp = (0xFFFFFFFF ^ int(instructions,2)) + 1
                value = int(twosComp) * -1
                data.append(value)
                dataPrint.append(value)

            elif int(instructions,2) >> 31 == 0:
                data.append(int(instructions,2))
                dataPrint.append(int(instructions,2))

            outFileDis.write(str(data[i]) + '\n')

        i += 1

def twosComplement(value, bits):
    if (value & (1 << (bits - 1))) != 0:
        value = value - (1 << bits)
    return value

def binaryToDecimal(instructions):
    decimal = int(instructions, 2)
    return decimal

inFileDis = open(inputFileName, 'r')
outFileDis = open(outputFileName + "_dis1.txt", 'w')

while True:
    instructions = inFileDis.readline()
    if instructions == '':
        break
    dissme = Disassembler()
    dissme.run()

inFileDis.close()
outFileDis.close()
