from symbol_table import *
import re


def calculateBranchOffset(targetAddress, locationCounter):
    pc = locationCounter + 8
    offset = targetAddress - pc
    return offset


def BinToHex(number):
    # print(number)
    n = int(number, 2)
    string = '0x' + str("{0:08x}".format(n))
    return string


def closestNumber(n, m):
    # Find the quotient
    q = int(n / m)

    # 1st possible closest number
    n1 = m * q

    # 2nd possible closest number
    if ((n * m) > 0):
        n2 = (m * (q + 1))
    else:
        n2 = (m * (q - 1))

        # if true, then n1 is the required closest number
    # if (abs(n - n1) < abs(n - n2)):
    # return n1

    # else n2 is the required closest number
    return n2


def assemble(text):
    # print("Call") #testing #success
    symtab_labels.clear()
    error = {'flag': False, 'type': '', 'lineNo': 1}
    errorList = []
    assembled = []
    Encoded = []
    errorFlag = False
    lineNumber = 1
    orgLineNumber = 1
    text = text.split('\n')
    # print('text: ', text)  # testing #success
    for i in text:
        if i is '':
            text.remove(i)
    # print('text2: ', text)  # testing #success
    if text[len(text) - 1] is '':
        text = text[:-1]
    # print('text3: ', text)  # testing #success

    # Pass One ---
    # Populates the symbol table with all
    # the user-defined labels encountered.
    locationCounter = 0
    for line in text:
        line1 = re.sub('\s+|,', '*', line)  # ;## print('a', line1)
        line1 = re.sub('\*+', '*', line1)  # ;##print('b', line1)
        lineList = line1.split('*')  # ;##print('c', line)
        # print(lineList)
        if lineList[1] == ";" or lineList[1][0] == ";":
            orgLineNumber += 1
            continue
        if '.' in lineList[1]:
            if lineList[1] in directiveList:
                if lineList[1].lower() == ".org":
                    locationCounter = int(lineList[2], 16)
                    asdLine = str(hex(locationCounter)) + '\t' + ','.join(lineList[1:])
                    assembled.append(asdLine)
                    orgLineNumber += 1
                    continue
                if lineList[1].lower() == ".space":
                    print('this is  a space')
                    size = int(lineList[2])
                    # print(size)
                    if size % 4 == 0:
                        asdLine = str(hex(locationCounter)) + '\t' + ','.join(lineList[1:])
                        assembled.append(asdLine)
                        locationCounter = locationCounter + size
                        orgLineNumber += 1
                        continue
                    else:
                        asdLine = str(hex(locationCounter)) + '\t' + ','.join(lineList[1:])
                        assembled.append(asdLine)
                        locationCounter = locationCounter + closestNumber(size, 4)
                        # print(locationCounter)
                        orgLineNumber += 1
                        continue
                if lineList[1].lower() == ".word":
                    print('this is  a word')
                    asdLine = str(hex(locationCounter)) + '\t' + ','.join(lineList[1:])
                    assembled.append(asdLine)
                    numOfWords = len(lineList[2:])
                    locationCounter = locationCounter + numOfWords * 4
                    orgLineNumber += 1
                    continue
                    # print(locationCounter)
                if lineList[1].lower() == ".byte":
                    print('this is  a byte')
                    count = len(lineList[2:])
                    # print(count)
                    if count % 4 == 0:
                        asdLine = str(hex(locationCounter)) + '\t' + ','.join(lineList[1:])
                        assembled.append(asdLine)
                        locationCounter = locationCounter + count
                        orgLineNumber += 1
                        continue
                    else:
                        asdLine = str(hex(locationCounter)) + '\t' + ','.join(lineList[1:])
                        assembled.append(asdLine)
                        locationCounter = locationCounter + closestNumber(count, 4)
                        orgLineNumber += 1
                        continue
                if lineList[1].lower() == ".hword":
                    print('this is  a hword')
                    count = len(lineList[2:])
                    # print(count)
                    if (count * 2) % 4 == 0:
                        asdLine = str(hex(locationCounter)) + '\t' + ','.join(lineList[1:])
                        assembled.append(asdLine)
                        locationCounter = locationCounter + count * 2
                        orgLineNumber += 1
                        continue
                    else:
                        asdLine = str(hex(locationCounter)) + '\t' + ','.join(lineList[1:])
                        assembled.append(asdLine)
                        locationCounter = locationCounter + closestNumber((count * 2), 4)
                        # print(closestNumber((count*2), 4))
                        orgLineNumber += 1
                        continue
                if lineList[1].lower() == ".end":
                    break

            else:
                print("here is invalid directive in line: ", orgLineNumber)
                errorFlag = True
                error.update(flag=True, type='Invalid Directive', lineNo=orgLineNumber)
                errorList.append(error.copy())
                orgLineNumber += 1
                locationCounter = locationCounter + 4
                continue
        elif ':' in lineList[1]:
            txt = lineList[1].rstrip(':')
            if txt in symtab_labels:
                print("Duplicate label in line: ", orgLineNumber)
                errorFlag = True
                error.update(flag=True, type='Duplicate label', lineNo=orgLineNumber)
                errorList.append(error.copy())
                orgLineNumber += 1
                locationCounter = locationCounter + 4
                continue
            symtab_labels[txt] = locationCounter
            if not lineList[2].lower() in opcodes:
                print("here is invalid OpCode in line: ", orgLineNumber)
                errorFlag = True
                error.update(flag=True, type='Invalid OpCode', lineNo=orgLineNumber)
                errorList.append(error.copy())
                orgLineNumber += 1
                locationCounter = locationCounter + 4
                continue

        elif not lineList[1].lower() in opcodes:
            print("here is invalid opcode in line: ", orgLineNumber)
            errorFlag = True
            error.update(flag=True, type='Invalid OpCode', lineNo=orgLineNumber)
            errorList.append(error.copy())
            orgLineNumber += 1
            locationCounter = locationCounter + 4
            continue

        asdLine = str(hex(locationCounter)) + '\t' + ','.join(lineList[1:])
        assembled.append(asdLine)
        orgLineNumber += 1
        locationCounter = locationCounter + 4

    if not errorFlag:
        with open('symbol_table.txt', 'w') as file:
            for item in symtab_labels:
                file.write(item + " " + str(hex(symtab_labels[item])) + "\n")

        with open('intermediate_file.txt', 'w') as file2:
            for item in assembled:
                file2.write("%s\n" % item)
        # print(locationCounter)
        # print(line)

    # ---------------------------------------------------End Of pass 1------------------------------------------------#

    # start of pass 2
    InstructionLine = {}
    with open("intermediate_file.txt") as f:
        for lin in f:
            (LC, Inst) = lin.split()
            InstructionLine[LC] = Inst
    orgLineNumber=1
    for LC in InstructionLine:
        Label_temp = ''
        line1 = re.sub('\s+|,', '*', InstructionLine[LC])  # ;## print('a', line1)
        line1 = re.sub('\*+', '*', line1)  # ;##print('b', line1)
        lineList = line1.split('*')  # ;##print('c', line)
        lineList.insert(0, '0')
        # print(lineList)
        Label_temp = ''

        if ':' in lineList[1]:
            Label_temp = lineList[1]
            del lineList[1]

        if lineList[1].lower() in opcodes:
            op = lineList[1].lower()
            cat = opcodes[op]
            if cat == 'REGOP':
                I = 0
                S = 0
                if len(op) > 3:
                    if len(op) == 4:
                        condition_machine = conditions['al']
                        if op[3] == 's':
                            S = 1
                    if len(op) == 6:
                        condition_machine = conditions[op[3:5]]
                        if op[5] == 's':
                            S = 1
                    if len(op) == 5:
                        condition_machine = conditions[op[3:]]
                else:
                    condition_machine = conditions['al']

                if op[:3] == 'teq' or op[:3] == 'tst' or op[:3] == 'mvn' or op[:3] == 'mov' or op[:3] == 'cmp' or op[
                                                                                                                  :3] == 'cmn':
                    numOfOperands = 2
                    if op[:3] == 'mvn' or op[:3] == 'mov':
                        # Immediate shifter_operand
                        if lineList[3][0] == '#':
                            I = 1
                            encode_imm = '0000'
                            if lineList[3][1:3].lower() == '0x':
                                imm_value = str("{0:08b}".format(int(lineList[3][1:], 16)))
                                # print(imm_value)
                            else:
                                imm_value = str("{0:08b}".format(int(lineList[3][1:])))
                                # print(imm_value)
                            op_machine = opcodesWithMachine[op[:3]]
                            instruction_machine = condition_machine + '00' + str(I) + op_machine + str(S) + '0000' + \
                                                  registers[lineList[2].lower()] + encode_imm + imm_value
                            print(BinToHex(instruction_machine))
                            asdLine = str(hex(locationCounter)) + str(lineList[1:])
                        elif lineList[3][0].lower() == 'r':
                            # Immediate shifts
                            lineLength = len(lineList)
                            # print(lineLength)
                            if lineLength == 4:
                                # <Rm>
                                op_machine = opcodesWithMachine[op[:3]]
                                instruction_machine = condition_machine + '00' + str(I) + op_machine + str(S) + '0000' + \
                                                      registers[
                                                          lineList[2].lower()] + '00000000' + registers[
                                                          lineList[3].lower()]
                                print(BinToHex(instruction_machine))
                            elif lineLength == 6:
                                # <Rm>,lsl#<shift_immediate>
                                if lineList[4][:3].lower() == 'lsl':
                                    # print('this is lsl')
                                    shift = '00'
                                elif lineList[4][:3].lower() == 'lsr':
                                    # print('this is lsr')
                                    shift = '01'
                                elif lineList[4][:3].lower() == 'asr':
                                    # print('this is asr')
                                    shift = '10'
                                elif lineList[4][:3].lower() == 'ror':
                                    # print('this is ror')
                                    shift = '11'

                                if lineList[5][0] == '#':
                                    if lineList[5][1:3].lower() == '0x':
                                        shift_imm = str("{0:05b}".format(int(lineList[5][1:], 16)))
                                        # print(imm_value)
                                    else:
                                        # print('integer')
                                        shift_imm = str("{0:05b}".format(int(lineList[5][1:])))
                                        # print(imm_value)

                                    op_machine = opcodesWithMachine[op[:3]]
                                    instruction_machine = condition_machine + '00' + str(I) + op_machine + str(
                                        S) + '0000' + \
                                                          registers[lineList[2].lower()] + shift_imm + shift + '0' + \
                                                          registers[
                                                              lineList[3].lower()]
                                    print(BinToHex(instruction_machine))

                                elif lineList[5][0].lower() == 'r':
                                    print(lineList[5])
                                    op_machine = opcodesWithMachine[op[:3]]
                                    instruction_machine = condition_machine + '00' + str(I) + op_machine + str(
                                        S) + '0000' + \
                                                          registers[lineList[2].lower()] + registers[
                                                              lineList[5].lower()] + '0' + shift + '1' + \
                                                          registers[lineList[3].lower()]
                                    print(BinToHex(instruction_machine))

                    else:
                        # Immediate shifter_operand 2 operands (cmp,cmn)
                        if lineList[3][0] == '#':
                            I = 1
                            encode_imm = '0000'
                            if lineList[3][1:3].lower() == '0x':
                                imm_value = str("{0:08b}".format(int(lineList[3][1:], 16)))
                                # print(imm_value)
                            else:
                                imm_value = str("{0:08b}".format(int(lineList[3][1:])))
                                # print(imm_value)
                            op_machine = opcodesWithMachine[op[:3]]
                            instruction_machine = condition_machine + '00' + str(I) + op_machine + str(1) + registers[
                                lineList[2].lower()] + '0000' + encode_imm + imm_value
                            print(BinToHex(instruction_machine))

                        elif lineList[3][0].lower() == 'r':
                            # Immediate shifts
                            lineLength = len(lineList)
                            # print(lineLength)
                            if lineLength == 4:
                                # <Rm>
                                op_machine = opcodesWithMachine[op[:3]]
                                instruction_machine = condition_machine + '00' + str(I) + op_machine + str(1) + \
                                                      registers[
                                                          lineList[2].lower()] + '0000' + '00000000' + registers[
                                                          lineList[3].lower()]
                                print(BinToHex(instruction_machine))
                            elif lineLength == 6:
                                # <Rm>,lsl#<shift_immediate>
                                if lineList[4][:3].lower() == 'lsl':
                                    # print('this is lsl')
                                    shift = '00'
                                elif lineList[4][:3].lower() == 'lsr':
                                    # print('this is lsr')
                                    shift = '01'
                                elif lineList[4][:3].lower() == 'asr':
                                    # print('this is asr')
                                    shift = '10'
                                elif lineList[4][:3].lower() == 'ror':
                                    # print('this is ror')
                                    shift = '11'

                                if lineList[5][0] == '#':
                                    if lineList[5][1:3].lower() == '0x':
                                        shift_imm = str("{0:05b}".format(int(lineList[5][1:], 16)))
                                        # print(imm_value)
                                    else:
                                        # print('integer')
                                        shift_imm = str("{0:05b}".format(int(lineList[5][1:])))
                                        # print(imm_value)

                                    op_machine = opcodesWithMachine[op[:3]]
                                    instruction_machine = condition_machine + '00' + str(I) + op_machine + str(1) + \
                                                          registers[
                                                              lineList[2].lower()] + '0000' + shift_imm + shift + '0' + \
                                                          registers[lineList[3].lower()]
                                    print(BinToHex(instruction_machine))

                                elif lineList[5][0].lower() == 'r':
                                    print(lineList[5])
                                    op_machine = opcodesWithMachine[op[:3]]
                                    instruction_machine = condition_machine + '00' + str(I) + op_machine + str(1) + \
                                                          registers[lineList[2].lower()] + '0000' + registers[
                                                              lineList[5].lower()] + '0' + shift + '1' + \
                                                          registers[lineList[3].lower()]
                                    print(BinToHex(instruction_machine))

                else:
                    numOfOperands = 3
                    # Immediate shifter_operand
                    if lineList[4][0] == '#':
                        I = 1
                        encode_imm = '0000'
                        if lineList[4][1:3].lower() == '0x':
                            imm_value = str("{0:08b}".format(int(lineList[4][1:], 16)))
                            # print(imm_value)
                        else:
                            imm_value = str("{0:08b}".format(int(lineList[4][1:])))
                            # print(imm_value)
                        op_machine = opcodesWithMachine[op[:3]]
                        instruction_machine = condition_machine + '00' + str(I) + op_machine + str(S) + registers[
                            lineList[3].lower()] + registers[lineList[2].lower()] + encode_imm + imm_value
                        print(BinToHex(instruction_machine))

                    elif lineList[4][0] == 'r':
                        # Immediate shifts
                        # Immediate shifts
                        lineLength = len(lineList)
                        # print(lineLength)
                        if lineLength == 5:
                            # <Rm>
                            op_machine = opcodesWithMachine[op[:3]]
                            instruction_machine = condition_machine + '00' + str(I) + op_machine + str(S) + registers[
                                lineList[3].lower()] + registers[lineList[2].lower()] + '00000000' + registers[
                                                      lineList[4].lower()]
                            print(BinToHex(instruction_machine))
                        elif lineLength == 7:
                            # <Rm>,lsl#<shift_immediate>
                            if lineList[5][:3].lower() == 'lsl':
                                # print('this is lsl')
                                shift = '00'
                            elif lineList[5][:3].lower() == 'lsr':
                                # print('this is lsr')
                                shift = '01'
                            elif lineList[5][:3].lower() == 'asr':
                                # print('this is asr')
                                shift = '10'
                            elif lineList[5][:3].lower() == 'ror':
                                # print('this is ror')
                                shift = '11'

                            if lineList[6][0] == '#':
                                if lineList[6][1:3].lower() == '0x':
                                    shift_imm = str("{0:05b}".format(int(lineList[6][1:], 16)))
                                    # print(imm_value)
                                else:
                                    # print('integer')
                                    shift_imm = str("{0:05b}".format(int(lineList[6][1:])))
                                    # print(imm_value)

                                op_machine = opcodesWithMachine[op[:3]]
                                instruction_machine = condition_machine + '00' + str(I) + op_machine + str(S) + \
                                                      registers[
                                                          lineList[3].lower()] + registers[
                                                          lineList[2].lower()] + shift_imm + shift + '0' + \
                                                      registers[lineList[4].lower()]
                                print(BinToHex(instruction_machine))

                            elif lineList[6][0].lower() == 'r':
                                print(lineList[6])
                                op_machine = opcodesWithMachine[op[:3]]
                                instruction_machine = condition_machine + '00' + str(I) + op_machine + str(S) + \
                                                      registers[
                                                          lineList[3].lower()] + registers[
                                                          lineList[2].lower()] + registers[
                                                          lineList[6].lower()] + '0' + shift + '1' + \
                                                      registers[lineList[4].lower()]
                                print(BinToHex(instruction_machine))

            elif cat == 'SWAP':
                B = 0
                if len(op) > 3:
                    if len(op) == 4:
                        condition_machine = conditions['al']
                        B = 1
                    if len(op) == 6:
                        condition_machine = conditions[op[3:5]]
                        B = 1
                    if len(op) == 5:
                        condition_machine = conditions[op[3:]]
                else:
                    condition_machine = conditions['al']

                instruction_machine = condition_machine + '00010' + str(B) + '00' + \
                                      registers[
                                          lineList[4][1:3].lower()] + registers[lineList[2].lower()] + \
                                      '00001001' + registers[lineList[3].lower()]
                print(BinToHex(instruction_machine))

            elif cat == 'TRANS':
                print('TRANS')
                I, P, U, B, W, L = 0, 1, 1, 0, 0, 0
                if len(op) > 3:
                    if len(op) == 4:
                        condition_machine = conditions['al']
                        B = 1
                    if len(op) == 6:
                        condition_machine = conditions[op[3:5]]
                        B = 1
                    if len(op) == 5:
                        condition_machine = conditions[op[3:]]
                else:
                    condition_machine = conditions['al']
                if op[:3] == 'ldr':
                    L = 1
                elif op[:3] == 'str':
                    L = 0
                instruction_machine = condition_machine + '01' + str(I) + str(P) + str(U) + str(B) + str(W) + str(L) + \
                                      registers[lineList[3][1:3].lower()] + registers[lineList[2].lower()] + \
                                      '000000000000'
                print(BinToHex(instruction_machine))

            elif cat == 'MULT':
                S = 0
                noOfoperand = len(lineList[2:])
                if len(op) > 3:
                    if len(op) == 4:
                        condition_machine = conditions['al']
                        if op[3] == 's':
                            S = 1
                    if len(op) == 6:
                        condition_machine = conditions[op[3:5]]
                        if op[5] == 's':
                            S = 1
                    if len(op) == 5:
                        condition_machine = conditions[op[3:]]
                else:
                    condition_machine = conditions['al']

                if op[2] == 'a':
                    if noOfoperand != 4:
                        print('mla must have 4 registers operands')  # Error
                        errorFlag = True
                        error.update(flag=True, type='Invalid No. of Operand', lineNo=orgLineNumber)
                        errorList.append(error.copy())
                        orgLineNumber += 1
                        continue
                    else:
                        A = 1
                        instruction_machine = condition_machine + '000000' + str(A) + str(S) + \
                                              registers[
                                                  lineList[2].lower()] + registers[lineList[5].lower()] + registers[
                                                  lineList[4].lower()] + '1001' + registers[lineList[3].lower()]
                        print(BinToHex(instruction_machine))
                else:
                    if noOfoperand != 3:
                        print('mul must have 3 registers operands')  # Error
                        errorFlag = True
                        error.update(flag=True, type='Invalid No. of Operand', lineNo=orgLineNumber)
                        errorList.append(error.copy())
                        orgLineNumber += 1
                        continue
                    else:
                        A = 0
                        instruction_machine = condition_machine + '000000' + str(A) + str(S) + \
                                              registers[
                                                  lineList[2].lower()] + '0000' + registers[
                                                  lineList[4].lower()] + '1001' + registers[lineList[3].lower()]
                        print(BinToHex(instruction_machine))

            elif cat == 'BRANCH':
                if len(op) == 3:
                    condition_machine = conditions[op[1:]]
                    L = 0
                elif len(op) == 4:
                    condition_machine = conditions[op[2:]]
                    L = 1
                elif len(op) == 1:
                    condition_machine = conditions['al']
                    L = 0
                elif len(op) == 2:
                    condition_machine = conditions['al']
                    L = 1
                if lineList[2].lower() in symtab_labels:
                    targetAdrs = symtab_labels[lineList[2].lower()]
                    offset = calculateBranchOffset(targetAdrs, int(LC, 16)) // 4
                    offset_binary = format(offset if offset >= 0 else (1 << 24) + offset, '024b')
                    instruction_machine = condition_machine + '101' + str(L) + offset_binary
                    # print(offset_binary)
                    print(BinToHex(instruction_machine))
                else:
                    print("here is undefined symbol in line: ", orgLineNumber)
                    errorFlag = True
                    error.update(flag=True, type='Undefined Symbol', lineNo=orgLineNumber)
                    errorList.append(error.copy())
                    orgLineNumber += 1
                    continue
            elif cat == 'SWI':
                if len(op) == 5:
                    condition_machine = conditions[op[3:]]
                else:
                    condition_machine = conditions['al']
                if lineList[2][:2].lower() == '0x':
                    imm_24 = str("{0:024b}".format(int(lineList[2], 16)))

                else:
                    imm_24 = str("{0:024b}".format(int(lineList[2])))

                instruction_machine = condition_machine + '1111' + imm_24
                print(BinToHex(instruction_machine))

            EncodedLine = LC + '\t' + BinToHex(instruction_machine) + '\t' + Label_temp + lineList[
                1] + ' ' + ','.join(lineList[2:])
            Encoded.append(EncodedLine)

        if lineList[1].lower() == ".space":
            size = int(lineList[2])
            locCtr = int(LC, 16)

            if size % 4 == 0:
                for i in range(size // 4):
                    EncodedLine = str(hex(locCtr)) + '\t' + '00000000' + '\t' + Label_temp + lineList[
                        1] + ' ' + ','.join(lineList[2:])
                    Encoded.append(EncodedLine)
                    locCtr += 4
            else:
                for i in range(closestNumber(size, 4) // 4):
                    EncodedLine = str(hex(locCtr)) + '\t' + '00000000' + '\t' + Label_temp + lineList[
                        1] + ' ' + ','.join(lineList[2:])
                    Encoded.append(EncodedLine)
                    locCtr += 4

        if lineList[1].lower() == ".word":
            numOfWords = len(lineList[2:])
            locCtr = int(LC, 16)
            for i in range(numOfWords):
                if lineList[i + 2][:2] == '0x':
                    value = int(lineList[i + 2], 16)
                else:
                    value = int(lineList[i + 2])
                EncodedLine = str(hex(locCtr)) + '\t' + str("{0:08x}".format(value)) + '\t' + Label_temp + \
                              lineList[
                                  1] + ' ' + ','.join(lineList[2:])
                Encoded.append(EncodedLine)
                locCtr += 4
        if lineList[1].lower() == ".byte":
            size = len(lineList[2:])
            temp = ''
            locCtr = int(LC, 16)
            if size % 4 == 0:
                for i in range(size // 4):
                    for j in range(4):
                        if lineList[j + 2][:2] == '0x':
                            value = int(lineList[j + 2], 16)
                            temp = temp + str("{0:02x}".format(value))
                        else:
                            value = int(lineList[j + 2])
                            temp = temp + str("{0:02x}".format(value))
                    EncodedLine = str(hex(locCtr)) + '\t' + temp + '\t' + Label_temp + lineList[
                        1] + ' ' + ','.join(lineList[2:])
                    Encoded.append(EncodedLine)
                    locCtr += 4
            else:
                counter = 0
                for i in range(closestNumber(size, 4) // 4):
                    temp = ''
                    for j in range(4):
                        try:
                            if lineList[j + counter + 2][:2] == '0x':
                                value = int(lineList[j + counter + 2], 16)
                                temp = temp + str("{0:02x}".format(value))
                            else:
                                value = int(lineList[j + counter + 2])
                                temp = temp + str("{0:02x}".format(value))

                        except:
                            print('hi')
                    counter += 4
                    EncodedLine = str(hex(locCtr)) + '\t' + temp + '\t' + Label_temp + lineList[
                        1] + ' ' + ','.join(lineList[2:])
                    Encoded.append(EncodedLine)
                    locCtr += 4

        if lineList[1].lower() == ".hword":
            temp = ''
            locCtr = int(LC, 16)
            count = len(lineList[2:])
            # print(count)
            if (count * 2) % 4 == 0:
                for i in range(count * 2 // 4):
                    for j in range(2):
                        if lineList[j + 2][:2] == '0x':
                            value = int(lineList[j + 2], 16)
                            temp = temp + str("{0:04x}".format(value))
                        else:
                            value = int(lineList[j + 2])
                            temp = temp + str("{0:04x}".format(value))
                    EncodedLine = str(hex(locCtr)) + '\t' + temp + '\t' + Label_temp + lineList[
                        1] + ' ' + ','.join(lineList[2:])
                    Encoded.append(EncodedLine)
                    locCtr += 4
            else:
                counter = 0
                for i in range(closestNumber(count * 2, 4) // 4):
                    temp = ''
                    for j in range(2):
                        try:
                            if lineList[j + counter + 2][:2] == '0x':
                                value = int(lineList[j + counter + 2], 16)
                                temp = temp + str("{0:04x}".format(value))
                            else:
                                value = int(lineList[j + counter + 2])
                                temp = temp + str("{0:04x}".format(value))

                        except:
                            print('hi')
                    counter += 2
                    EncodedLine = str(hex(locCtr)) + '\t' + temp + '\t' + Label_temp + lineList[
                        1] + ' ' + ','.join(lineList[2:])
                    Encoded.append(EncodedLine)
                    locCtr += 4
        orgLineNumber += 1
    print('labels - ', symtab_labels)  # testing #status
    print('Errors - ', errorList)

    if not errorFlag:
        with open('Listing_file.txt', 'w') as file:
            for item in Encoded:
                file.write(item + "\n")

        with open('Object_file.txt', 'w') as file:
            for item in Encoded:
                file.write(item.rsplit('\t', 1)[0] + "\n")
    return (lineNumber - 1), Encoded, errorList, errorFlag

# assemble("1 swi 15")
