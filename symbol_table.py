# reading opcodes and their machine code in a dictionary for pass-2
opcodes = {}
with open("opcodes2.txt") as f:
    for line in f:
        (key, val) = line.split()
        opcodes[key] = val

# for x in opcodes:
#     print (x)
#     print (opcodes[x])

directiveList = [".org", ".end", ".space", ".byte", ".hword", ".word"]
# with open("opcodes.txt") as f:
#     opcodes = [line.rstrip() for line in f]

registers = {"r0": "0000", "r1": "0001", "r2": "0010", "r3": "0011", "r4": "0100", "r5": "0101", "r6": "0110",
             "r7": "0111", "r8": "1000",
             "r9": "1001", "r10": "1010", "r11": "1011", "r12": "1100", "r13": "1101", "r14": "1110", "r15": "1111"}

opcodesWithMachine = {'and': '0000', 'eor': '0001', 'sub': '0010', 'rsb': '0011', 'add': '0100', 'adc': '0101',
                      'sbc': '0110', 'rsc': '0111', 'tst': '1000', 'teq': '1001', 'cmp': '1010', 'cmn': '1011',
                      'orr': '1100',
                      'mov': '1101', 'bic': '1110', 'mvn': '1111'}

conditions = {'eq': '0000', 'ne': '0001', 'cs': '0010', 'hs': '0010', 'cc': '0011', 'lo': '0011', 'mi': '0100',
              'pl': '0101', 'vs': '0110',
              'vc': '0111', 'hi': '1000', 'ls': '1001', 'ge': '1010', 'lt': '1011', 'gt': '1100', 'le': '1101',
              'al': '1110'}

symtab_labels = {}
