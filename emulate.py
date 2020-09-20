import re
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


def compile_code(code, display_result=False):
    print("[#] Compiling...")
    code = code.split("\n") # split into commands
    code = [i for i in code if i] # remove blank lines
    new_code = []

    # remove comments
    for c, line in enumerate(code):
        clean = line
        clean = clean.split("#")[0].strip()
        new_code.append(clean)
    code = new_code
    
    
    variables = code[code.index("end")+1:]
    # replace variable names
    
    for index, var in enumerate(variables):
        
        name, value = var.split(":")
        #print(index, name, value)
        code = "\n".join(code)
        code = code.replace(f"{name}\n", f"{str(index)}\n")
        code = code.replace(f"{name} ", f"{str(index)} ")
        code = code.replace(f"{name}:", "")
        code = code.split("\n")
    
    new_code = []
    # handle goto pointes of the form :pointer:
    pointers = re.findall(r":\w+:", "\n".join(code))
    pointers = list(dict.fromkeys(pointers)) # remove duplicates
    for pointer in pointers:
        pointer_addr = [c for c,p in enumerate(code) if p == pointer][0]
        code[pointer_addr] = f"#{pointer}"
        code = "\n".join(code).replace(pointer, str(pointer_addr))
        code = code.split("\n")
    
    print("[#] Code Compiled!")
    #print("\n".join(code))
    if display_result:
        print("\n".join(code))
    return "\n".join(code)







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
        # note data adresses start at 0 from "end" onwards. goto uses the true addr
        # so the first command is addr 0
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
        if cmd[0] == "pow": # pow [addr]
            mdr = int(code[int(cmd[1])+offset])
            ac **= mdr
        if cmd[0] == "mod": # pow [addr]
            mdr = int(code[int(cmd[1])+offset])
            ac %= mdr
        
        
        
        if cmd[0] == "out": # out
            print(ac)
        if cmd[0] == "inp": # inp
            ac = int(input())
        
        
        if cmd[0] == "store": # store [addr]
            # stores accumulator value in specified adress
            code[int(cmd[1])+offset] = ac

        if cmd[0] == "goto": # goto [addr] []
            pc = int(cmd[1])-1
        if cmd[0] == "halt":
            break
        
        if cmd[0] == "eq": # eq [addr]
            ac = int(ac == int(code[int(cmd[1])+offset]))


        # eq ==
        # neq !=
        # les <
        # leq <=
        # gre >
        # geq >=

        if cmd[0] == "if":
            if (
                ((ac == int(code[int(cmd[2])+offset])) if cmd[1] == "==" else False)
                or ((ac != int(code[int(cmd[2])+offset])) if cmd[1] == "!=" else False)
                or ((ac < int(code[int(cmd[2])+offset])) if cmd[1] == "<" else False)
                or ((ac <= int(code[int(cmd[2])+offset])) if cmd[1] == "<=" else False)
                or ((ac > int(code[int(cmd[2])+offset])) if cmd[1] == ">" else False)
                or ((ac >= int(code[int(cmd[2])+offset])) if cmd[1] == ">=" else False)
            ):
                pc = int(cmd[4])-1


        if debug:
            print(f"\tAccumulator: {acc_old} -> {ac}\n\tMDR {mdr_old} -> {mdr}\n\tMAR {mar_old} -> {mar}")
            mem = code[code.index("end")+1:]
            print("\tMEM:", mem, end="\n\n")

        pc += 1
#emulate(code)