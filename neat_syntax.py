from emulate import emulate, compile_code
# figure out a way to implement if statements
# maybe: if == [addr] goto [addr]
#       [   if statement   ]   [other command] 
code = """
:loop:
load var # this is a comment
add inc
store var
pow power
out

load var

if < lim goto :loop:

end

var:0
inc:1
lim:10
power:2
"""
code = compile_code(code)
emulate(code, False)