from emulate import emulate, compile_code
# figure out a way to implement if statements
# maybe: if == [addr] goto [addr]
#       [   if statement   ]   [other command] 
# The following code outputs the squares of number 1-10
#
code = """
:start:
load one 
store md # set md to 1
load count
add inc # inccrement count (current number)
store count
if > lim goto :end: # if past limit end program


:check_prime: # looped to check if prime
load md
add inc # increment mod value
store md
if == count goto :prime: # if found no factors: print number

load md


load count
mod md # modulo
if == zero goto :start: # if a factor was found, the number isn't prime: go to next number


load md
if < count goto :check_prime: # if not checked all possible factors then check next one

:prime:
load count
out # if prime: output number and go to next number if not at limit
if < lim goto :start:

:end:
end
count:1
inc:1
lim:100
md:1
zero:0
one:1
"""
code = compile_code(code)
emulate(code, False)