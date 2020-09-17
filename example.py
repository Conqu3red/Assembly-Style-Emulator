from emulate import emulate

code = """
inp
store 0
inp
store 1
load 0
add 1
out
end
0
0
"""
emulate(code, False)