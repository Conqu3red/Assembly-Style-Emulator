from emulate import emulate, compile_code
# figure out a way to implement if statements
# maybe: if == [addr] goto [addr]
#       [   if statement   ]   [other command] 
code = """
load 0
add 1
store 0
pow 3
out

load 0

if < 2 goto 0

end

0
1
10
2
"""
compile_code(code)
#emulate(code, False)