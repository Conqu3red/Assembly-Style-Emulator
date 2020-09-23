import PySimpleGUI as sg
import emulate

examples = {
	"Primes":""":start:
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
one:1"""
}








code_frame = [
				  [sg.Multiline(size=(30, 15), key='input')]
			   ]
compiled_frame = [
				  [sg.Multiline(size=(30, 15), key='compiled')]
			   ]
output_frame = [
				  [sg.Multiline(size=(30, 15), key='output')]
			   ]


sg.theme('SystemDefaultForReal')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Assembly - Style Emulator')],
			[sg.Frame('Code', code_frame, font='Any 12'), sg.Frame('Compiled Code', compiled_frame, font='Any 12'), sg.Frame('Output', output_frame, font='Any 12')],
			[sg.Button('Emulate'), sg.Button('Load example')]]

def get_example():
	options = ["Primes"]
	layout = [[sg.Text('Choose an Example:')],
				[sg.Combo(["Primes"], default_value="Primes")],
			  [sg.OK()]]

	window = sg.Window('Second Form', layout)
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
			break 
		if values[0] in options:
			window.close()
			return values[0]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
		break
	if event == "Load example":
		example = get_example()
		if example in examples.keys():
			window.Element("input").update(value=examples[example])
	if event == "Emulate":
		code = emulate.compile_code(values['input'])
		window.Element("compiled").update(value=code)
		#emulate(code, False)

window.close()