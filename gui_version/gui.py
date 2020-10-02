import PySimpleGUI as sg
import emulate
import os

import tkinter as tk
from tkinter import filedialog




sg.theme('SystemDefaultForReal')   # Add a touch of color

code_frame = [
				  [sg.Multiline(size=(30, 15), key='input', change_submits=True)]
			   ]
compiled_frame = [
				  [sg.Multiline(size=(30, 15), key='compiled')]
			   ]
output_frame = [
				  [sg.Multiline(size=(40, 15), key='output')]
			   ]

menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],            
            ['Help', 'About'], ]

prog_input_frame = [[sg.Input(disabled=True,size=(30, 1),background_color="light green", key="program_input"), sg.Button("Send Input", disabled=True)]]
inp = sg.Frame("Input", prog_input_frame, pad=(250,0),font="Helvetica 12")

examples = ["Choose an Example program"] + os.listdir("examples")


# All the stuff inside your window.
layout = [  [sg.Menu(menu_def)],
			[sg.Text('Assembly Style Emulator', font='Helvetica 25')],
			[],
			[sg.Frame('Code', code_frame, font='Helvetica 12'), sg.Frame('Compiled Code', compiled_frame, font='Helvetica 12'), sg.Column([[sg.Frame('Output', output_frame, font='Helvetica 12')]])],
			[sg.Button('Emulate'), sg.Combo(examples,tooltip="Choose an example program to load", default_value="Choose an Example program", key="load_example", readonly=True, change_submits=True),sg.Button("", visible=False,size=(30,1)), inp],
			[sg.Checkbox("Debug", key="show_debug"),sg.Checkbox("Live Compile", key="live_compile")]]


def request_input():
	global window
	window.Element("program_input").update(disabled=False)
	window.Element("Send Input").update(disabled=False)
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
			window.close()
			break
		if event == 'Send Input':
			window.Element("program_input").update(disabled=True)
			window.Element("program_input").update(value="")
			window.Element("Send Input").update(disabled=True)
			return values['program_input']
		
# Create the Window
window = sg.Window('Assembly Style Emulator', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	#print(event)
	if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
		break

	# toolbar presses
	if event == "Open":
		root = tk.Tk()
		root.withdraw()

		file_path = filedialog.askopenfilename(defaultextension=".asf",filetypes=((("Assembly-Style Files","*.asf"),("All files","*.*"))))
		if file_path:
			with open(file_path, "r") as f:
				data = f.read()
			window.Element("input").update(value=data) 
	
	if event == "Save":
		root = tk.Tk()
		root.withdraw()

		file_path = filedialog.asksaveasfilename(defaultextension=".asf",filetypes=((("Assembly-Style Files","*.asf"),("All files","*.*"))))
		data = window.Element("input").get()
		if file_path:
			with open(file_path, "w") as f:
				f.write(data)
	if event == "About":
		sg.Popup("Version 2.0.1")
	# main

	if event == "input":
		if window.Element("live_compile").get():
			# update compiled code
			window.Element("compiled").update(background_color="white")
			code, error = emulate.compile_code(values['input'])
			window.Element("compiled").update(value=code)
			if error:
				window.Element("compiled").update(background_color="red")

	if event == "load_example":
		example = window.Element("load_example").get()
		if example != "Choose an Example program":
			with open(f"examples/{example}", "r") as f:
				program = f.read()
			window.Element("input").update(value=program)
	
	if event == "Emulate":
		window.Element("compiled").update(background_color="white")
		window.Element("output").update(background_color="white")

		code, error = emulate.compile_code(values['input'])
		window.Element("compiled").update(value=code)
		#window.Element("program_input").update(disabled=False)
		window.Element("output").update(value="")
		
		if error:
			window.Element("compiled").update(background_color="red")
		else:
			debug = window.Element("show_debug").get()
			# Emulate code
			code = code.split("\n") # split into commands
			code = [i for i in code if i] # remove blank lines
			ac = 0
			mar = 0
			mdr = 0
			pc = 0
			while pc <= code.index("end"):
				try:
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
						window.Element("output").update(value=f"\t[{instruction}]\n", append=True)
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
						window.Element("output").update(value=f"{ac}\n", append=True)
					if cmd[0] == "inp": # inp
						ac = int(request_input())


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
						window.Element("output").update(value=f"\tAC: {acc_old} -> {ac}\n\tMDR {mdr_old} -> {mdr}\n\tMAR {mar_old} -> {mar}\n", append=True)
						mem = code[code.index("end")+1:]
						window.Element("output").update(value=f"\tMEM: {','.join([str(l) for l in mem])}\n\n", append=True)

					pc += 1
				except Exception as e:
					window.Element("output").update(value=f"{e}\n", append=True, background_color="red")
					break

window.close()