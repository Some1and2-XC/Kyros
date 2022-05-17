#!/usr/bin/env python3

from PIL import Image

import os
from random import randint

from math import cos
from colorsys import hsv_to_rgb
from numba import jit

import turtle

from .ExecTime import *


class fractal:

	def __init__(self):

		self.__version__ = "v3.0.4"
		self.line = "-" * 25

		# Makes File Name with Four Letters Between "A" and "Z" : ABCD.txt
		self.FileName = "".join( chr(randint(65, 90)) for i in range(4) )
		self.ZoomAmnt = 2

		self.win = None

		# Used to specify wether the make Three Dee version
		self.TD = False

		try:
			os.mkdir(self.FileName)
		except:
			pass
		os.chdir(self.FileName)

	# Main function for Running Turtles
	def main(self, x: float = 0, y: float = 0, first: bool = False):

		self.eval(turtle = True)

		return

	@ExecTime
	# Function that evaluates and draws graph
	def eval(self, turtle: bool = False):

		# Makes SizeY the correct amount of pixels in relation to SizeX
		self.SizeY = int((self.BoxRange[0][1] / self.BoxRange[0][0]) * self.SizeX)


		if turtle:
			# Gets which Percentage of the Screen that was Clicked on
			self.clickLocation = (2 * x / self.SizeX, 2 * y / self.SizeY)

			# if this is not the first click, this is used to make the start conditions easier to setup
			# This makes some ajustments to where the boxrange is after you click (zooming twice as close and moving)
			if not first:
				self.BoxRange = ((self.BoxRange[0][0] / self.ZoomAmnt, self.BoxRange[0][1] / self.ZoomAmnt), (self.BoxRange[1][0] + (self.BoxRange[0][0] - (self.BoxRange[0][0] / self.ZoomAmnt)) / 2 + self.BoxRange[0][0] * self.clickLocation[0] / self.ZoomAmnt, self.BoxRange[1][1] + (self.BoxRange[0][1] - (self.BoxRange[0][1] / self.ZoomAmnt)) / 2 + self.BoxRange[0][1] * self.clickLocation[1] / self.ZoomAmnt))

		self.WriteFileInformation()

		# Setting Up Image
		im = Image.new("RGBA", (self.SizeX, self.SizeY), (255, 255, 255, 255))
		pixel = im.load()

		# Sets 'oneline' to the line of values generated in 'MakeFrame' and 'i' to which line it had made (counting from 0 to SizeX - 1)
		# Only generated one line of the frame at a time into memory at a time instead of generating the entire image. 

		print(f"\n{self.FileName}\n{self.line}")

		data = []

		# O(n) for memory usage
		# (for the variables defined, image data is still O(n^2) (Obvious reasons))

		for (oneline, i) in self.MakeFrame():
			data.append(oneline)
			for j in range(self.SizeX):
				pixel[j, self.SizeY - i - 1] = self.ColorIn(oneline[j])

		# prints the time it took to complete
		print(f"\n{self.line}")

		# Gets text added to the actual file that is Saved
		savedFile = f"{self.FileName} - {self.count}.png"

		# Saves Image
		im.save(savedFile)

		if self.win is not None:
			# Sets the background of the Turtle window as the newly created image
			self.win.bgpic(savedFile)

			# Updates the Turtle Screen
			self.win.update()

		if self.TD:
			TDObject(self.FileName, data, self.ColorIn, self.MaxI, self.ColorType, self.RateOfColorChange).eval()

		return

	# Function for printing Header
	def PrintHeader(self):
		print(f"{self.__version__} - {self.FileName}\n{self.line}")
		return

	# Function For setting all the variables in the Fractal (through `input()` commands)
	def GetData(self):

		def IntInput(message: str) -> int:
			while True:
				try:
					out = int(input(message))
					return out
				except:
					print("Invalid Input")

		def FloatInput(message: str) -> float:
			while True:
				try:
					out = float(input(message))
					return out
				except:
					print("Invalid Input")

		def TupleInput(message1: str, message2: str, mode: str) -> tuple:
			while True:
				out1 = str2tuple(input(message1))
				out2 = str2tuple(input(message2))
				if out1 is not False and out2 is not False:
					if mode == "Coordinate":
						# For if you want a fractal between two coordinates
						# where out1 is the bottom left and out2 is top right
						return ((abs(out1[0] - out2[0]), abs(out1[1] - out2[1])), out1)

					if mode == "Range":
						# out1 is bottom left and out2 is the distance
						return (out2, out1)
				else:
					print("Invalid Input")

		def str2tuple(txt: str):
			# removes "(" and ")" from String, replaces , with spaces then splits on the spaces then takes the floating point value of what is in each part of the list, 
			# then returns it as a tuple
			try:
				return tuple(float(i) for i in "".join(i for i in txt if i != "(" and i != ")").replace(",", " ").split())

			except:
				return False

		self.IsJulia = input("Generate JS? (y/n) (q is Usually Best): ")

		if len(self.IsJulia) != 0 and self.IsJulia.lower()[0] == "q":
			# Defines all starting parameters
			self.SetAll()
			return

		self.count = IntInput("Count [Starting Index of the Image]: ")
		self.SizeX = IntInput("Resolution [px]: ")
		self.RateOfColorChange = FloatInput("Rate Of color Change (9 is Usually Best): ")
		self.MaxI = IntInput("Maximum Iterations (~1000 is Usually Best): ")
		self.BoxRange = TupleInput("Enter Coordinate of Bottom Left ((-2, -2) is Usually Best): ", "Enter Coordinate of Range ((4, 4) is Usually Best): ", "Range")

		if len(self.IsJulia) != 0 and self.IsJulia.lower()[0] == "y":
			ci = FloatInput("What is your imaginary 'c' value: ")
			self.cj = FloatInput("What is your real 'c' value: ")
			self.IsJulia = True

		else:
			self.ci = 0
			self.cj = 0
			self.IsJulia = False

		gens = ["SD IT", "SD TD", "R IT", "R TD", "BS IT", "BS TD", "ABR IT", "ABR TD"]
		self.GenType = input("Generator Type (SD TD is Usually Best): ")
		if self.GenType not in gens:
			self.GenType = "SD IT"

		colors = ["basic", "sunset", "ocean", "fire"]
		self.ColorType = input("Color Type (basic is Usually Best): ")
		if self.ColorType not in colors:
			self.ColorType = "basic"

		self.WriteHeader()
		self.GetFunction()

		return

	# Defines all starting parameters
	def SetAll(self, settings: dict = None):
		if settings == None:

			settings = {
				"count": 0,
				"ci": 0,
				"cj": 0,
				"IsJulia": False,
				"SizeX": 512,
				"MaxI": 1000,
				"RateOfColorChange": 9,
				"BoxRange": ((4, 4), (-2, -2)),
				"GenType": "SD IT",
				"ColorType": "basic"
			}

		self.count = settings["count"]
		self.ci = settings["ci"]
		self.cj = settings["cj"]
		self.IsJulia = settings["IsJulia"]
		self.SizeX = settings["SizeX"]
		self.MaxI = settings["MaxI"]
		self.RateOfColorChange = settings["RateOfColorChange"]
		self.BoxRange = settings["BoxRange"]
		self.GenType = settings["GenType"]
		self.ColorType = settings["ColorType"]

		self.WriteHeader()
		self.GetFunction()

		return

	# Writes Header Information to the Data file
	def WriteHeader(self):
		genTxt =  [
		"Some1and2's Kyros - A Fractal Generator",
		" SD | Standard (f(z) = z^2 + c)",
		"  R | Rabbit (Subtract Real Number from Imaginary and Vise Versa with f(z) = z^2 + c)",
		" BS | Burning Ship (f(z) = |z|^2)",
		"ABR | Absolute Rabbit (Subract Real Number from Imaginary and Vise Versa with f(z) = |z|^2 + c)",
		"",
		" IT | Makes function based on itteration count",
		" TD | Makes function based on travel distance",
		"",
		"colors = basic|sunset|ocean|fire",
		"",
		"Ex: ",
		"SD TD",
		"Makes Standard f(z) = z^2 | based on Travel Distance",
		""
		]

		genTxt = "\n".join(genTxt)

		with open(f"{self.FileName}.md", "a") as text:
			text.write(f"{genTxt}{self.FileName} | {self.ColorType} | {self.GenType}\n{self.line}")
			text.close()

		return

	# Writes information about each File that is Generated
	def WriteFileInformation(self):

		# Defines the text to add to the Image information file
		self.name = "Set "
		if self.IsJulia:
			self.name += f"({self.cj} + {self.ci}i) "

		NameInfo = [
		f"(Resolution = {self.SizeX / 1000}k)", 
		f"(Rate = {self.RateOfColorChange})", 
		f"(Iterations = {self.MaxI})", 
		f"(Range = {self.BoxRange[1]} -", 
		f"{(self.BoxRange[1][0] + self.BoxRange[0][0], self.BoxRange[1][1] + self.BoxRange[0][1])})", 
		f"(Distance = {self.BoxRange[0]})"
		]

		# Adds all the Segments of the Information into the `name` Variable
		self.name += " ".join( segment for segment in NameInfo )
		
		del NameInfo

		with open(f"{self.FileName}.md", "a") as text:
			text.write(f"\n{self.count} | {self.name}")
			text.close()

		return

	# Sets self.MagicFunctionGenerator to the correct function
	def GetFunction(self):

		if self.GenType == "SD TD":

			@jit(nopython=True)
			def MagicFunctionGenerator(MaxI, cj, ci, zj, zi):
				#Magic Generator Function  (b is the number of itterations)
				DeltaDistance = 0
				r = 2
				for b in range(MaxI):
					yout = 2 * zi * zj + ci
					xout = zj ** 2 - zi ** 2 + cj
					if yout * yout + xout * xout > r ** 2:
						break
					DeltaDistance += ((yout - zi) ** 2 + (xout - zj) ** 2) ** .5
					zi = yout
					zj = xout

				if b == 0:
					return 0

				elif b == MaxI - 1:
					return MaxI - 1

				elif zj != xout:


					# Formula for x value of intersection point of a circle and a line

					# -mb +- sqrt(r^2(m^2 + 1) - b^2)
					# ------------------------------- = x
					#			 m^2 + 1

					# m and b are from y = mx + b (linear equation standard form)

					# m = DeltaY / DeltaX
					m = (yout - zi) / (xout - zj)

					# b = y - mx
					b = yout - m * xout

					# inside = sqrt(m^2r^2 + r^2 - b^2)
					inside = (r ** 2 * (m ** 2 + 1) - b ** 2) ** .5

					OutNum = (- m * b + inside) / (m ** 2 + 1)

					# If the point is not between zj and xout then the point found is the incorrect intersection
					# point
					if not zj <= OutNum <= xout or zj >= OutNum >= xout:
						OutNum -= 2 * inside / (m ** 2 + 1)

					DeltaDistance += ((OutNum - zj) ** 2 + (OutNum * m + b - zi) ** 2) ** .5
				
				else:
					# If both x's are the same then the m value in y = mx + b will be n / 0
					# This finds instead where the circle would be at the x value then subtracts the
					# found value which solves the 'divide by zero' issue


					# R will always be bigger than xout because in this if statment 
					# xout == zj which will always be within the 2 radius
					outNo = (r ** 2 - xout ** 2) ** .5

					if not zi <= outNo <= yout:
						outNo *= -1

					DeltaDistance += abs(outNo - zi)
					# return MaxI - 1

				return DeltaDistance

		elif self.GenType == "R IT":
			@jit(nopython=True)
			def MagicFunctionGenerator(MaxI, cj, ci, zj, zi):
				#Magic Generator Function  (b is the number of itterations)
				for b in range(MaxI):
					yout = zi * zj * 2 + ci - zj
					xout = zj ** 2 - zi ** 2 + cj - zi
					if yout * yout + xout * xout > 4:
						break
					zi = yout
					zj = xout
				return b

		elif self.GenType == "R TD":
			@jit(nopython=True)
			def MagicFunctionGenerator(MaxI, cj, ci, zj, zi):
				#Magic Generator Function  (b is the number of itterations)
				DeltaDistance = 0
				r = 2
				for b in range(MaxI):
					yout = 2 * zi * zj + ci - zj
					xout = zj ** 2 - zi ** 2 + cj - zi
					if yout * yout + xout * xout > r ** 2:
						break
					DeltaDistance += ((yout - zi) ** 2 + (xout - zj) ** 2) ** .5
					zi = yout
					zj = xout

				if b == 0:
					return 0

				elif b == MaxI - 1:
					return MaxI - 1

				elif zj != xout:


					# Formula for x value of intersection point of a circle and a line

					# -mb +- sqrt(r^2(m^2 + 1) - b^2)
					# ------------------------------- = x
					#			 m^2 + 1

					# m and b are from y = mx + b (linear equation standard form)

					# m = DeltaY / DeltaX
					m = (yout - zi) / (xout - zj)

					# b = y - mx
					b = yout - m * xout

					# inside = sqrt(m^2r^2 + r^2 - b^2)
					inside = (r ** 2 * (m ** 2 + 1) - b ** 2) ** .5

					OutNum = (- m * b + inside) / (m ** 2 + 1)

					# If the point is not between zj and xout then the point found is the incorrect intersection
					# point
					if not zj <= OutNum <= xout or zj >= OutNum >= xout:
						OutNum -= 2 * inside / (m ** 2 + 1)

					DeltaDistance += ((OutNum - zj) ** 2 + (OutNum * m + b - zi) ** 2) ** .5

				else:
					# If both x's are the same then the m value in y = mx + b will be n / 0
					# This finds instead where the circle would be at the x value then subtracts the
					# found value which solves the 'divide by zero' issue


					# R will always be bigger than xout because in this if statment 
					# xout == zj which will always be within the 2 radius
					outNo = (r ** 2 - xout ** 2) ** .5

					if not zi <= outNo <= yout:
						outNo *= -1

					DeltaDistance += abs(outNo - zi)
					# return MaxI - 1

				return DeltaDistance

		elif self.GenType == "BS IT":

			@jit(nopython=True)
			def MagicFunctionGenerator(MaxI, cj, ci, zj, zi):
				#Magic Generator Function  (b is the number of itterations)
				r = 2
				for b in range(MaxI):
					yout = abs(2 * zi * zj) + ci
					xout = zj ** 2 - zi ** 2 + cj
					if yout * yout + xout * xout > r ** 2:
						break
					zi = yout
					zj = xout
				return b

		elif self.GenType == "BS TD":

			@jit(nopython=True)
			def MagicFunctionGenerator(MaxI, cj, ci, zj, zi):
				#Magic Generator Function  (b is the number of itterations)
				DeltaDistance = 0
				r = 2
				for b in range(MaxI):
					yout = abs(2 * zi * zj) + ci
					xout = zj ** 2 - zi ** 2 + cj
					if yout * yout + xout * xout > r ** 2:
						break
					DeltaDistance += ((yout - zi) ** 2 + (xout - zj) ** 2) ** .5
					zi = yout
					zj = xout

				if b == 0:
					return 0

				elif b == MaxI - 1:
					return MaxI - 1

				elif zj != xout:


					# Formula for x value of intersection point of a circle and a line

					# -mb +- sqrt(r^2(m^2 + 1) - b^2)
					# ------------------------------- = x
					#			 m^2 + 1

					# m and b are from y = mx + b (linear equation standard form)

					# m = DeltaY / DeltaX
					m = (yout - zi) / (xout - zj)

					# b = y - mx
					b = yout - m * xout

					# inside = sqrt(m^2r^2 + r^2 - b^2)
					inside = (r ** 2 * (m ** 2 + 1) - b ** 2) ** .5

					OutNum = (- m * b + inside) / (m ** 2 + 1)

					# If the point is not between zj and xout then the point found is the incorrect intersection
					# point
					if not zj <= OutNum <= xout or zj >= OutNum >= xout:
						OutNum -= 2 * inside / (m ** 2 + 1)

					DeltaDistance += ((OutNum - zj) ** 2 + (OutNum * m + b - zi) ** 2) ** .5

				else:
					# If both x's are the same then the m value in y = mx + b will be n / 0
					# This finds instead where the circle would be at the x value then subtracts the
					# found value which solves the 'divide by zero' issue


					# R will always be bigger than xout because in this if statment 
					# xout == zj which will always be within the 2 radius
					outNo = (r ** 2 - xout ** 2) ** .5

					if not zi <= outNo <= yout:
						outNo *= -1

					DeltaDistance += abs(outNo - zi)
					# return MaxI - 1

				return DeltaDistance

		elif self.GenType == "ABR IT":
			@jit(nopython=True)
			def MagicFunctionGenerator(MaxI, cj, ci, zj, zi):
				#Magic Generator Function  (b is the number of itterations)
				for b in range(MaxI):
					yout = abs(2 * zi * zj) + ci - zj
					xout = zj ** 2 - zi ** 2 + cj - zi
					if yout * yout + xout * xout > 4:
						break
					zi = yout
					zj = xout
				return b

		elif self.GenType == "ABR TD":
			@jit(nopython=True)
			def MagicFunctionGenerator(MaxI, cj, ci, zj, zi):
				#Magic Generator Function  (b is the number of itterations)
				DeltaDistance = 0
				r = 2
				for b in range(MaxI):
					yout = abs(2 * zi * zj) + ci - zj
					xout = zj ** 2 - zi ** 2 + cj - zi
					if yout * yout + xout * xout > r ** 2:
						break
					DeltaDistance += ((yout - zi) ** 2 + (xout - zj) ** 2) ** .5
					zi = yout
					zj = xout

				if b == 0:
					return 0

				elif b == MaxI - 1:
					return MaxI - 1

				elif zj != xout:


					# Formula for x value of intersection point of a circle and a line

					# -mb +- sqrt(r^2(m^2 + 1) - b^2)
					# ------------------------------- = x
					#			 m^2 + 1

					# m and b are from y = mx + b (linear equation standard form)

					# m = DeltaY / DeltaX
					m = (yout - zi) / (xout - zj)

					# b = y - mx
					b = yout - m * xout

					# inside = sqrt(m^2r^2 + r^2 - b^2)
					inside = (r ** 2 * (m ** 2 + 1) - b ** 2) ** .5

					OutNum = (- m * b + inside) / (m ** 2 + 1)

					# If the point is not between zj and xout then the point found is the incorrect intersection
					# point
					if not zj <= OutNum <= xout or zj >= OutNum >= xout:
						OutNum -= 2 * inside / (m ** 2 + 1)

					DeltaDistance += ((OutNum - zj) ** 2 + (OutNum * m + b - zi) ** 2) ** .5

				else:
					# If both x's are the same then the m value in y = mx + b will be n / 0
					# This finds instead where the circle would be at the x value then subtracts the
					# found value which solves the 'divide by zero' issue


					# R will always be bigger than xout because in this if statment 
					# xout == zj which will always be within the 2 radius
					outNo = (r ** 2 - xout ** 2) ** .5

					if not zi <= outNo <= yout:
						outNo *= -1

					DeltaDistance += abs(outNo - zi)
					# return MaxI - 1

				return DeltaDistance

		else:
			@jit(nopython=True)
			def MagicFunctionGenerator(MaxI, cj, ci, zj, zi):
				#Magic Generator Function  (b is the number of itterations)
				r = 2
				for b in range(MaxI):
					yout = 2 * zi * zj + ci
					xout = zj ** 2 - zi ** 2 + cj
					if yout * yout + xout * xout > r ** 2:
						break
					zi = yout
					zj = xout
				return b

		# Returns the function without calling it, this makes it such that any variable set to generators.ReturnFunction("Type") is set to the MagicFunctionGenerator defined in this file
		self.MagicFunctionGenerator = MagicFunctionGenerator
		del MagicFunctionGenerator
		return

	# Lets functions made by user be able to be used instead of prebuilt
	def SetFunction(self, func):
		1
		self.MagicFunctionGenerator = lambda *args: (func(args[1]) - args[2])

	# Function for making each frame
	def MakeFrame(self):
		for i in range(int(self.SizeY + .5)):
			line = []
			for j in range(self.SizeX):
				# Gets Generator Values based on relative position of BoxRange
				if self.IsJulia is False:
					self.ci = i * self.BoxRange[0][1] / (self.SizeY - 1) + self.BoxRange[1][1]
					self.cj = j * self.BoxRange[0][0] / (self.SizeX - 1) + self.BoxRange[1][0]
					self.zi = 0
					self.zj = 0


				if self.IsJulia is True:
					self.zi = i * self.BoxRange[0][1] / (self.SizeY - 1) + self.BoxRange[1][1]
					self.zj = j * self.BoxRange[0][0] / (self.SizeX - 1) + self.BoxRange[1][0]
				
				# Magic Generator Function (b is the number of itterations)
				b = self.MagicFunctionGenerator(self.MaxI, self.cj, self.ci, self.zj, self.zi)

				line.append(b)

			print("{spaces}{CurrentWorkingNumber} / {TotalNumber} | {percentage:.2f}%".format(spaces=" " * (len(str(self.SizeY)) - len(str(i + 1))), CurrentWorkingNumber=i + 1, TotalNumber=self.SizeY, percentage=100 * (i + 1) / self.SizeY), end="\r")
			# fuckin' gamer yield
			yield (line, i)

	# Function that returns color based on Previous settings an `b` value
	def ColorIn(self, b: float) -> tuple:

		def ToRadians(n):
			return n * 3.141592653589792323 / 180

		if b != 0:
			if b == (self.MaxI) - 1:
				OutColor = (0, 0, 0, 255)
			else:
				if self.ColorType == "sunset":
					MinValue = 277
					MaxValue = 420
					hue = ((MaxValue - MinValue) * .5 * cos(ToRadians(b * self.RateOfColorChange)) + (MaxValue + MinValue) * .5) % 360
					value = .125 * cos(ToRadians(b * self.RateOfColorChange)) + .815

				elif self.ColorType == "ocean":
					MinValue = 14
					MaxValue = 255
					hue = ((MaxValue - MinValue) * .5 * cos(ToRadians(b * self.RateOfColorChange + 180)) + (MaxValue + MinValue) * .5) % 360
					value = .125 * cos(ToRadians(b * self.RateOfColorChange)) + .815
					value = 1

				elif self.ColorType == "fire":
					MinValue = -40 # aka 320
					MaxValue = 65
					hue = ((MaxValue - MinValue) * .5 * cos(ToRadians(b * self.RateOfColorChange)) + (MaxValue + MinValue) * .5) % 360
					value = .125 * cos(ToRadians(b * self.RateOfColorChange)) + .815

				elif self.ColorType == "red":
					MinValue = -20
					MaxValue = 25
					hue = ((MaxValue - MinValue) * .5 * cos(ToRadians(b * self.RateOfColorChange)) + (MaxValue + MinValue) * .5) % 360
					value = .125 * cos(ToRadians(b * self.RateOfColorChange)) + .815

				else:
					hue = (b * self.RateOfColorChange)
					value = 1

				
				OutColor = tuple(int(i * 255) for i in (*hsv_to_rgb(hue / 360, 1, value), 1))
		else:
			OutColor = (255, 255, 255, 0)
		return OutColor

	# Function for setting up turtle screen
	def TurtleSetup(self):
		# Sets up turtle screen to Match the file Generated Ratio
		self.win = turtle.Screen()
		self.win.setup(self.SizeX, int((self.BoxRange[0][1] / self.BoxRange[0][0]) * self.SizeX))
		self.win.tracer(0, 0)
		self.win.title(f"{self.__version__} - {self.FileName}")

		# Makes any key that is pressed close the window
		self.win.listen()
		for i in range(35, 127):
			self.win.onkeypress(self.close, chr(i))

		self.main(first = True)

		self.win.onclick(self.main)
		self.win.mainloop()

		return

	# Function for opening buttons as an overlay for turtle screen
	def OpenTurtleMenu(self):
		1
		pass

	# Function for Closing Turtles
	def close(self):
		self.win.bye()
		exit()

class TDObject:
	def __init__(self, name: str,  data: list = [[0, 1],[1, 2]], ColorFunc = False, MaxI: int = 1000, ColorType: str = "basic", RateOfColorChange: int = 9):
		self.name = name
		self.data = data
		self.ColorFunc = ColorFunc
		self.MaxI = MaxI
		self.ColorType = ColorType
		self.RateOfColorChange = RateOfColorChange

	# Function for evaluating
	def eval(self):

		# Actual Dimensions of end Image
		self.imX = int(1024 * 8)
		self.imY = int(self.imX * 9 / 16)

		# Dimensions of the list supplied
		self.xLen = len(self.data)
		self.yLen = len(self.data[0])

		self.yHeightMultiplyer = 0.5 * self.xLen / self.MaxI

		def WriteInitialisation(n):
			1
			print(f"3D INITIALISATION: [{n} / 3]", end="\r")

		WriteInitialisation(1)
		triangles = self.CubicTriangleAssembly()
		WriteInitialisation(2)
		# Data becomes list of triangle corners with coordinates
		self.data = self.SquaredTriangleAssembly(triangles)
		WriteInitialisation(3)

		print()
		print("-" * 25)

		BackgroundColor = (255, 255, 255, 0)
		im = Image.new("RGBA", (self.imX, self.imY), BackgroundColor)
		pixel = im.load()

		# Returns a list of the bottom left + top right of the triangle
		def GetBox(data):
			Box = [list(data[0]), list(data[1])]
			for i in data:
				if i[0] < Box[0][0]:
					Box[0][0] = i[0]

				if i[1] < Box[0][1]:
					Box[0][1] = i[1]

				if i[0] > Box[1][0]:
					Box[1][0] = i[0]

				if i[1] > Box[1][1]:
					Box[1][1] = i[1]

			return Box


		# Function for seeing if a particular point is within the triangle data
		def IsInATriangle(data, PointTuple):
			(x, y) = PointTuple
			del PointTuple

			# Making system of equations to find if a point is between the three coordinates
			(A, B, C) = data["data"]

			if IsBetween(A, B, C, x, y):
				if IsBetween(B, C, A, x, y):
					if IsBetween(C, A, B, x, y):
						return (True, data["color"])
			return (False, 0)

		# Sees if C is on the same side of A and B as the point (x, y)
		# m & b variables are variables used in y = mx + b
		@jit(nopython=True)
		def IsBetween(A, B, C, x, y):
			if B[0] == A[0]:
				if (A[0] >= C[0]) == (A[0] >= x):
					return True
				return False
			
			else:
				m = (B[1] - A[1]) / (B[0] - A[0])
				b = A[1] - m * A[0]

				if (C[1] >= m * C[0] + b) == (y >= m * x + b):
					return True

				if y == m * x + b:
					return True

				return False

		for i in range(len(self.data)):
			print(f"{i + 1} / {len(self.data)} | {100 * (i + 1) / len(self.data):.2f}%   ", end="\r")
			i = self.data[i]

			# Gets the extreme corners of a triangle to find a box to search for pixels within
			Box = GetBox(i["data"])

			# Number to multiply the Box values by
			Mult = [self.imX / self.xLen, self.imY / self.yLen]

			Box = [ [ int(Box[i][j] * Mult[j]) for j in range(2) ] for i in range(2) ]

			del Mult

			# Adding one to each range so that the last pixel found in 'Box' is searched
			for j in range(Box[0][0], Box[1][0] + 1):
				# makes sure j is in range
				if 0 < j <= self.imX:
					for k in range(Box[0][1], Box[1][1] + 1):
						# makes sure k is in range
						if 0 < k <= self.imY:
							# IsInATriangle() returns [bool, ColorValue] which is why if statement looks for n[0]
							n = IsInATriangle(i, (j * self.xLen / self.imX, k * self.yLen / self.imY))
							if n[0]:
								try:
									if 0 <= self.imY - k - 1 < self.imY:
										# Sets Pixel to the color of n[1] which is the color value
										pixel[j, self.imY - k - 1] = n[1]
								except:
									1
		im.save(f"{self.name}-3D.png")
		print()
		print("-" * 25)
		return

	# Function for formatting the data such that the triangles are accessable to the other functions, makes `data` into a list of triangles in 3D space
	def CubicTriangleAssembly(self):
		for i in range(self.xLen - 1):
			for j in range(self.yLen - 1):
				if self.data[i][j] != 0:
					# more gamer coding
					yield {
						"data":((i, j, self.data[i][j] * self.yHeightMultiplyer), (i+1, j, self.data[i+1][j] * self.yHeightMultiplyer), (i, j+1, self.data[i][j+1] * self.yHeightMultiplyer)),
						"color": self.ColorFunc(self.data[i][j])
					}
					yield {
						"data":((i+1, j+1, self.data[i+1][j+1] * self.yHeightMultiplyer), (i, j+1, self.data[i][j+1] * self.yHeightMultiplyer), (i+1, j, self.data[i+1][j] * self.yHeightMultiplyer)),
						"color": self.ColorFunc(self.data[i][j])
					}
		return

	# Takes the info from CubicTriangleAssembly then transforms into 2D linear equations for boundries of triangles
	def SquaredTriangleAssembly(self, triangles):
		# Makes 2D Triangles out of 3D array
		return [{"data": self.TransformFunc(i["data"]), "color": i["color"]} for i in triangles][::-1]

	# Function for the math to make the points from 3D to 2D
	def TransformFunc(self, triuple: tuple):
		# Just cosine of 30 degrees
		cosN = 0.866025403784
		sinN = 0.5
		responces = []
		for n in triuple:
			# responces.append((j - i + xLen) * .5, (j * sinN + i * sinN + index) / (cosN * 2))
			responces.append(((n[1] - n[0] + self.xLen) * .5, (n[1] * sinN + n[0] * sinN + n[2]) / (cosN * 2)))
		return tuple(responces)
