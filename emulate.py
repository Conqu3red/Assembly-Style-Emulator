'''
language: kinda assembly except a bit different because I don't know assembly

command
load 5
[command] [addr]
'''

'''
code = """load 0
add 1
out
end
10
1"""
'''

code = """
inp
add 0
store 0
out
load 0
add 1
store 0
out
end
10
15"""

'''
inp # ask for input
add 0 # add var 0 (10) to input
store 0 # store in var 0
out # output ac
load 0 # load var 0
add 1 # add var 1 (15)
store 0 # store in var 0
out # output ac
end # end of codew
10 # var 0
15 # var 1
'''






# registers
mar = 0
mdr = 0
ac = 0
pc = 0
cir = 0




def emulate(code, debug=True):
    code = code.split("\n") # split into commands
    code = [i for i in code if i] # remove blank lines
    ac = 0
    mar = 0
    mdr = 0
    pc = 0
    while pc <= code.index("end"):
        instruction = code[pc]
        acc_old = ac
        mar_old = mar
        mdr_old = mdr
        mar = pc
        cmd = instruction.split(" ")
        offset = code.index("end")+1
        #print(instruction + ": Accumulator", ac, "MDR", mdr, "MAR", mar)
        if debug:
            print(f"\t[{instruction}]")
        if cmd[0] == "load": # load [addr]
            ac = int(code[int(cmd[1])+offset])
            mdr = ac
        if cmd[0] == "add": # add [addr]
            mdr = int(code[int(cmd[1])+offset])
            ac += mdr
        if cmd[0] == "sub": # sub [addr]
            mdr = int(code[int(cmd[1])+offset])
            ac -= mdr
        if cmd[0] == "mul": # mul [addr]
            mdr = int(code[int(cmd[1])+offset])
            ac *= mdr
        if cmd[0] == "div": # div [addr]
            mdr = int(code[int(cmd[1])+offset])
            ac /= mdr
        if cmd[0] == "out": # out
            print(ac)
        if cmd[0] == "inp": # inp
            ac = int(input())
        if cmd[0] == "store": # store [addr]
            # stores accumulator value in specified adress
            code[int(cmd[1])+offset] = ac

        if cmd[0] == "goto": # goto [addr]
            pc = int(cmd[1])
        
        if cmd[0] == "eq": # eq [addr]
            ac = int(ac == int(code[int(cmd[1])+offset]))


        if debug:
            print(f"\tAccumulator: {acc_old} -> {ac}\n\tMDR {mdr_old} -> {mdr}\n\tMAR {mar_old} -> {mar}")
            mem = code[code.index("end")+1:]
            print("\tMEM:", mem, end="\n\n")

        pc += 1
#emulate(code)