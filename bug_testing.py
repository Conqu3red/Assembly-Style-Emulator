from emulate import emulate, compile_code
# figure out a way to implement if statements
# maybe: if == [addr] goto [addr]
#       [   if statement   ]   [other command] 
# The following code outputs the squares of number 1-10
code = """
load var
load varb
load varb#comment
load varb #comment
load var # comment
out
end
var:0
varb:0
"""
code = compile_code(code, True)
emulate(code, False)