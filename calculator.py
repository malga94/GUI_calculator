import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from functools import partial

class MainWindow(qtw.QWidget):

	possible_operations = ['+', '-', '*', '/', '.', '^', '(', ')']
	values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	operation = ''

	def __init__(self):
		super().__init__()

		self.setWindowTitle("My awesome calculator")
		self.resize(500,500)
		self.main_layout = qtw.QVBoxLayout()
		self.setLayout(self.main_layout)

		self.screen = qtw.QLabel('Welcome')
		self.main_layout.addWidget(self.screen)

		self.screen.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Minimum)
		self.screen.setFont(qtg.QFont('Arial',32))

		self.create_buttons()

		self.show()

	def create_buttons(self):
		"""Very useful way to create a set of widgets which are all more or less the same"""
		self.buttons = {}
		buttons_layout = qtw.QGridLayout()
		buttons = {
			'^':(0,0),
			'(':(0,1),
			')':(0,2),
			'/':(0,3),
			'7':(1,0),
			'8':(1,1),
			'9':(1,2),
			'*':(1,3),
			'4':(2,0),
			'5':(2,1),
			'6':(2,2),
			'-':(2,3),
			'1':(3,0),
			'2':(3,1),
			'3':(3,2),
			'+':(3,3),
			'0':(4,0),
			'.':(4,1),
			'C':(4,2),
			'=':(4,3),
			'del':(4,4),
		}
		for btntext, pos in buttons.items():
			
			self.buttons[btntext] = qtw.QPushButton(btntext)
			#Connecting signals to the appropriate slots
			if btntext in self.values or btntext in self.possible_operations:
				"""Here we use partial (from functools) to pass an argument to the slot. Notice that you cannot use a lambda function, as it will pass the current value of btntext, 
				which after the buttons have been setup is always '=' (ie the key of the last button defined)"""
				self.buttons[btntext].clicked.connect(partial(self.prep_operation, btntext))

			elif btntext == 'C':
				 self.buttons[btntext].clicked.connect(self.clear_screen)

			elif btntext == '=':
				self.buttons[btntext].clicked.connect(self.do_operation)

			elif btntext == 'del':
				self.buttons[btntext].clicked.connect(self.del_value)

			#sizing the various buttons
			self.buttons[btntext].setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
			buttons_layout.addWidget(self.buttons[btntext], pos[0], pos[1])

		self.main_layout.addLayout(buttons_layout)

	def prep_operation(self, val):
		
		l = len(self.operation)
		if l == 0:
			if val in self.values + ['(', ')']:
				self.operation += val
				self.screen.setText(self.operation)
			else:
				pass
				
			return

		"""f we are storing the result of the previous operation, then we clear the screen if the user enters a new digit, or we use the result of the previous operation 
		if the user enters an operator (+,-,*...)"""
		if self.operation[-1] == '_':
			self.operation = self.operation[:-1]
			if val in self.possible_operations:
				self.operation += val 
			else:
				self.operation = val
			self.screen.setText(self.operation)
			return

		try:
			x = int(val)
			self.operation += val 
		except ValueError:
			if val == ('(' or ')'):
				self.operation += val
			elif self.operation[l-1] not in self.possible_operations:
				self.operation += val
			else:
				self.operation = self.operation[:-1]
				self.operation += val
		except Exception as e:
			self.screen.setText(f"Error: {str(e)}")

		self.screen.setText(self.operation)

	#Function that performes the operation stored in self.operation, called when the "=" button is pressed
	def do_operation(self):
		
		try:
			result = eval(self.operation.replace('^', '**'), {"__builtins__": {}}, {})
		except:
			result = "Error"
		self.screen.setText(str(result))
		self.operation = str(result) + '_'

	#Simply clears the screen and resets self.operation to an empty string: called when the clear (C) button is pressed
	def clear_screen(self):
		self.screen.setText('')
		self.operation = ''

	#Function called when the delete button is pressed. Removes one char from self.operation, and does nothing if it is empty
	def del_value(self):
		if len(self.operation) == 0:
			return
		if self.operation == 'Error_':
			self.clear_screen()
		#If the user has just hit enter, the underscore is appended to the operation string to change the behaviour of the "prepare_operation slot". 
		#We need to delete that and the previous character
		elif self.operation[-1] == '_':
			self.operation = self.operation[:-2]
		else:
			self.operation = self.operation[:-1]
		print(self.operation)
		self.screen.setText(self.operation)

if __name__ == '__main__':
	app = qtw.QApplication(sys.argv)
	mw = MainWindow()
	sys.exit(app.exec())