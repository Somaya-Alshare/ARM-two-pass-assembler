from symbol_table import *
import re


def addLeadingZeroes(string, length):
    while len(string) < length:
        string = "0" + string
    return string


def assemble(text):
    ###print("Call") #testing #success
    error = {'flag': False, 'type': '', 'lineNo': 1}
    errorList = []
    assembled = []
    errorFlag = False
    lineNumber = 1
    orgLineNumber = 1
    text = text.split('\n')
    ###print('text: ', text) #testing #success
    for i in text:
        if i is '':
            text.remove(i)
    ###print('text2: ', text) #testing #success
    if text[len(text) - 1] is '':
        text = text[:-1]
    ###print('text3: ', text) #testing #success

    '''
    Pass One ---
    Populates the symbol table with all 
    the user-defined labels encountered.
    '''
    for line in text:
        line1 = re.sub('\s+|,', '*', line)  # ;##print('a', line)
        line1 = re.sub('\*+', '*', line1)  # ;##print('b', line)
        lineList = line1.split('*')  # ;##print('c', line)
        if ':' in lineList[1]:
            symtab_labels[lineList[1]] = lineNumber
        lineNumber += 1
    # print('labels - ', symtab_labels) #testing #status

    '''
    Pass Two ---
    Performs the actual assembly of the code
    referring the symbol table.
    '''
    lineNumber = 1
    for line in text:
        # print(lineNumber)
        line = re.sub('\s+|,', '*', line)  # ;##print('a', line)
        line = re.sub('\*+', '*', line)  # ;##print('b', line)
        line = line.split('*')  # ;##print('c', line)
        line = line[1:]
        # print('line test:', line) #testing #success
        asdLine = ''  # assembled lines
        extraLine = ''  # the extra line for immediate mode

        # Symbol Table Look-up.
        # Opcode
        index = 0
        if line[0] not in symtab_opcode:
            if line[0] in symtab_labels:
                index = 1

            else:
                errorFlag = True
                error.update(flag=True, type='Invalid OpCode', lineNo=orgLineNumber)
                errorList.append(error)
                continue

        if line[index + 0] not in symtab_opcode:
            errorFlag = True
            error.update(flag=True, type='Invalid OpCode', lineNo=orgLineNumber)
            errorList.append(error)
            continue
        else:
            asdLine += addLeadingZeroes(bin(symtab_opcode.get(line[index + 0]))[2:], 4)
        ##print('opcode:', asdLine) #testing opcode #success

        ##print("Comes here 49")

        ##print('swi line:', line[0])
        if line[index + 0] == 'swi':

            if line[index + 1] not in symtab_swi:
                errorFlag = True
                error.update(flag=True, type='Invalid SWI Code', lineNo=orgLineNumber)
                errorList.append(error)
                continue
            else:
                ##print("Comes here 56")
                asdLine += addLeadingZeroes(bin(symtab_swi.get(line[index + 1]))[2:], 2)
                ##print('swi1:', asdLine)
                asdLine += '0000000000'  # 10 unused bits in the end
                ##print('swi2:', asdLine)

        ##print("Comes here 61")
        if line[index + 0] == 'mov':
            if line[index + 1] not in symtab_reg:
                errorFlag = True
                error.update(flag=True, type='Invalid Register Specified', lineNo=orgLineNumber)
                errorList.append(error)
                continue
            else:
                asdLine += addLeadingZeroes(bin(symtab_reg.get(line[index + 1]))[2:], 3)
                if '#' in line[index + 2]:
                    asdLine += '1'
                    while len(asdLine) < 16:
                        asdLine += '0'
                    extraLine = bin(int(line[index + 2][1:]))[2:]
                    extraLine = addLeadingZeroes(extraLine, 16)
                    ##print('extraline:', extraLine)
                else:
                    if line[index + 2] not in symtab_reg:
                        errorFlag = True
                        error.update(flag=True, type='Invalid Register Specified', lineNo=orgLineNumber)
                        errorList.append(error)
                        continue
                    else:
                        asdLine += addLeadingZeroes(bin(symtab_reg.get(line[index + 2]))[2:], 3)
                        while len(asdLine) < 16:
                            asdLine += '0'
                ##print('mov: ', asdLine)

        if line[index + 0] in dpi:
            if line[index + 1] not in symtab_reg:
                errorFlag = True
                error.update(flag=True, type='Invalid Register Specified', lineNo=orgLineNumber)
                errorList.append(error)
                continue
            else:
                asdLine += addLeadingZeroes(bin(symtab_reg.get(line[index + 1]))[2:], 3)
                if line[index + 2] not in symtab_reg:
                    errorFlag = True
                    error.update(flag=True, type='Invalid Register Specified', lineNo=orgLineNumber)
                    errorList.append(error)
                    continue
                else:
                    asdLine += addLeadingZeroes(bin(symtab_reg.get(line[index + 2]))[2:], 3)
                    if '#' in line[index + 3]:
                        asdLine += '1'
                        while len(asdLine) < 16:
                            asdLine += '0'
                        extraLine = bin(int(line[index + 3][1:]))[2:]
                        extraLine = addLeadingZeroes(extraLine, 16)
                        ##print('extraline:', extraLine)
                    else:
                        if line[index + 3] not in symtab_reg:
                            errorFlag = True
                            error.update(flag=True, type='Invalid Register Specified', lineNo=orgLineNumber)
                            errorList.append(error)
                            continue
                        else:
                            asdLine += addLeadingZeroes(bin(symtab_reg.get(line[index + 3]))[2:], 3)
                            while len(asdLine) < 16:
                                asdLine += '0'

        if line[index + 0] in cfi:
            temp_label = line[index + 1] + ':'
            if temp_label not in symtab_labels:
                errorFlag = True
                error.update(flag=True, type='Invalid Label Specified', lineNo=orgLineNumber)
                errorList.append(error)
                continue
            else:
                asdLine += addLeadingZeroes(bin(symtab_labels.get(temp_label))[2:], 12)
                while len(asdLine) < 16:
                    asdLine += '0'

        if line[index + 0] in dti:
            if line[index + 1] not in symtab_reg:
                errorFlag = True
                error.update(flag=True, type='Invalid Register Specified', lineNo=orgLineNumber)
                errorList.append(error)
                continue
            else:
                asdLine += addLeadingZeroes(bin(symtab_reg.get(line[index + 1]))[2:], 3)
                regex = re.match('\s*\[.*\]\s*', line[index + 2])
                # print('regex - ', regex, ' --- line(2) - (', line[index + 2])
                if regex is not None:
                    if line[index + 2][1:-1] not in symtab_reg:
                        errorFlag = True
                        error.update(flag=True, type='Invalid Register Specified', lineNo=orgLineNumber)
                        errorList.append(error)
                        continue
                    else:
                        asdLine += addLeadingZeroes(bin(symtab_reg.get(line[index + 2][1:-1]))[2:], 3)
                        while len(asdLine) < 16:
                            asdLine += '0'
                    ##print('extraline:', extraLine)
                else:
                    errorFlag = True
                    error.update(flag=True, type='Invalid Memory Location Specified', lineNo=orgLineNumber)
                    errorList.append(error)
                    continue

        assembled.append(asdLine)
        orgLineNumber += 1
        lineNumber += 1
        if extraLine is not '':
            assembled.append(extraLine)
            lineNumber += 1
            ###print(assembled, '\n', errorList, '\n', errorFlag)

    return (lineNumber - 1), assembled, errorList, errorFlag

    ###print(line) #testing #success
