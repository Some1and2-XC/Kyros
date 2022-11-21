#!/usr/bin/env python3

"""
Main file holding the `fractal` class
"""
from PIL import Image

# Imports for File Information
import os

# Imports for Drawing to the Screen
import turtle

# Relative Imports
from . import printutils as pu
from .math import GetFunction
from .coloring import color
from .ThreeDeeify import TDObject
from .videoify import videoify
from .ExecTime import ExecTime


class fractal:

	def __init__(self, FileName: str = None):

		"""
		Main Function for initialising Fractal Generation
		"""

		from random import randint

		self.__version__ = "v0.0.0"
		self.line = "-" * 25
		self.TD = False # Used to specify wether the make Three Dee version

		# Turtle Settings
		self.ZoomAmnt = 2 # The amount that the image zooms each click (with turtle / web version)
		self.win = None # window variable for turtle

		# Sets filename
		if FileName: self.FileName = FileName
		else: self.FileName = "F -- " + "".join( chr(randint(65, 90)) for i in range(4) ) # Makes File Name with Four Letters Between "A" and "Z" : ABCD.txt

		try: os.mkdir(self.FileName) # Tries to make a directory with called `self.FileName`
		except FileExistsError: ...  # If the file already exists, do nothing

		# Sets `self.FileName` to the folder that contains the files
		self.FileName = f"{self.FileName}\\{self.FileName}"

	@ExecTime
	def eval(self, turtle: bool = False, x: float = None, y: float = None, first = True, n = None):

		"""
		Function for evaluating the settings of the fractal
		& saving the image

		## Inputs
		 - Turtle: 

		returns -> tuple : (2D_Imagedata, 3D_Imagedata)
		###### (Returns only (2D_Imagedata, None) if `self.TD` is set to False)
		"""

		# Sets SizeY based on what SizeX is (this should be a seperate function)
		self.SizeY = int((self.BoxRange[0][1] / self.BoxRange[0][0]) * self.SizeX)

		if not first:
			"""
			## `clickLocation` is a tuple of which Percentage of the Screen that was Clicked on
			 - This makes some ajustments to where the boxrange is after you click (zooming twice as close and moving)
			 - This doesn't run every time to have the initial image generated being based on initial values
			"""

			clickLocation = (2 * x / self.SizeX, 2 * y / self.SizeY)
			self.BoxRange = (
				(
					self.BoxRange[0][0] / self.ZoomAmnt, # Sets Math X length value (distance between left and right)
					self.BoxRange[0][1] / self.ZoomAmnt  # Sets Math Y length value (distance between bottom and top)
				), 
				(
					self.BoxRange[1][0] + (self.BoxRange[0][0] - (self.BoxRange[0][0] / self.ZoomAmnt)) / 2 + self.BoxRange[0][0] * clickLocation[0] / self.ZoomAmnt, # Sets the Math leftmost value
					self.BoxRange[1][1] + (self.BoxRange[0][1] - (self.BoxRange[0][1] / self.ZoomAmnt)) / 2 + self.BoxRange[0][1] * clickLocation[1] / self.ZoomAmnt  # Sets the Math bottomost value
				)
			)

		# Write File Information to file
		pu.WriteFileInformation(self.FileName, self.count, self.ci, self.cj, self.IsJulia, self.SizeX, self.MaxI, self.BoxRange, self.GenType)

		# Sets up PIL Image object
		im = Image.new("RGBA", (self.SizeX, self.SizeY), (255, 255, 255, 255))
		pu.PrintHeader(self.__version__, self.FileName, self.count)

		data = [i for i in self.MakeFrame()]
		im.putdata( [ self.ColorIn(i) for i in data ] )
		pu.InfoOut() # adds a new line to the terminal output because the `MakeFrame` function uses `print(end="\r")`
		pu.line()
		savedFile = f"{self.FileName} - #{self.count}.png"
		im.save(savedFile)

		if self.win:
			"""
			Sets the Background of the turtle window as the generated image
			then updates the turtle window
			"""
			self.win.bgpic(savedFile)
			self.win.update()

		if self.TD:
			"""
			If the `self.TD` option is set to `True`, a 3D version is
			generated from the `ThreeDeeify.py` file
			
			Otherwise TDO is set to None

			"""

			# The dimension of the array has to be resized to make sure that the `TDObject().eval()` gets the right kind of data
			outdata = []
			for i in range(self.SizeY):
				outdata.append([])
				for j in range(self.SizeX):
					outdata[i].append(data[i * self.SizeX + j])

			# The problem is probably caused by the fact that you are passing in "data" which has been converted to its `self.ColorIn(i)` of `for i in self.MakeFrame()`
			TDO = TDObject(f"{self.FileName} - {self.count}", outdata, self.ColorIn, self.MaxI, n = self.count).eval()
		else: TDO = None

		self.count += 1

		# Returns the data of the two images that could be generated from `self.eval()`
		return (im, TDO)

	def MakeFrame(self):
		"""
		Function for generating each frame
		Returns a generator that only evaluates the math when it is necessary
		yields a value based on MagicFunctionGenerator
		"""

		for i in range(int(self.SizeY + .5)):
			line = []
			for j in range(self.SizeX):
				# Gets Generator Values based on relative position of BoxRange
				if self.IsJulia is False:
					self.ci = i * self.BoxRange[0][1] / (self.SizeY - 1) + self.BoxRange[1][1]
					self.cj = j * self.BoxRange[0][0] / (self.SizeX - 1) + self.BoxRange[1][0]
					zi = 0
					zj = 0
				if self.IsJulia is True:
					zi = i * self.BoxRange[0][1] / (self.SizeY - 1) + self.BoxRange[1][1]
					zj = j * self.BoxRange[0][0] / (self.SizeX - 1) + self.BoxRange[1][0]
				
				# Magic Generator Function (b is the number of itterations)
				yield self.MagicFunctionGenerator(self.MaxI, self.cj, self.ci, zj, zi)

			# Calls printutils.InfoOut for "Printing Values"
			pu.InfoOut("{spaces}{CurrentWorkingNumber} / {TotalNumber} | {percentage:.2f}%".format(
					spaces               = " " * (len(str(self.SizeY)) - len(str(i + 1))),
					CurrentWorkingNumber = i + 1,
					TotalNumber          = self.SizeY,
					percentage           = 100 * (i + 1) / self.SizeY
				),
				end="\r"
			)
		if self.IsJulia is False: self.ci = self.cj = 0

	def main(self, x: float = 0, y: float = 0, first: bool = False):
		# Main function for Running Turtles
		self.eval(turtle = True, x = x, y = y, first = first)
		return

	def SetAll(self, settings: dict = None, clr = None):
		# Defines all starting parameters
		"""
		Defines all Starting Parameters

		settings :: a dictionary of all the settings to be passed to the generator
		clr      :: a `color` object that has all the parameters set to be able to create color generation settings
		"""

		if settings is None:
			settings = {
				"count": 0,
				"ci": 0,
				"cj": 0,
				"IsJulia": False,
				"SizeX": 512,
				"MaxI": 1000,
				"BoxRange": ((4, 4), (-2, -2)),
				"GenType": "SD IT"
			}

		if not clr:
			# clr is the local function name for the color class
			# `color` is already set by the imported class

			clr = color(
				RateOfColorChange = 9,
				ColorStyle = "rotational",
				ShadowStyle = "none"
			)

		# Fractal Attributes
		self.count = settings["count"]
		self.ci = settings["ci"]
		self.cj = settings["cj"]
		self.IsJulia = settings["IsJulia"]
		self.SizeX = settings["SizeX"]
		self.MaxI = settings["MaxI"]
		self.BoxRange = settings["BoxRange"]
		self.GenType = settings["GenType"]

		self.color = clr

		# Sets the `self.color` `MaxI` attribute after everything is set

		if not self.color.MaxI:
			self.color.MaxI = self.MaxI

		self.WriteHeader()
		self.GetFunction()

	def WriteHeader(self):
		# Writes Header Information to the Data file
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
			"colors = [ basic | sunset | ocean | fire ]",
			"",
			"Ex: ",
			"SD TD",
			"Makes Standard f(z) = z^2 | based on Travel Distance",
			""
		]

		genTxt = "\n".join(genTxt) # Adds all the lines of genTxt list to a string separated by `\n`
		genTxt += f"\n{self.color.ReturnText()}\n" # Adds color information from the `self.color()` class
		genTxt += "\n" + " | ".join( \
			f"{text} : {str(value)}" for text, value in [ \
				["Name", self.FileName],
				["GenType", self.GenType],
				["TD Copy", self.TD]
			]
			if value
		) # Adds more information

		genTxt += f"\n{self.line}"
		with open(f"{self.FileName}.md", "a") as text:
			text.write(genTxt)
			text.close()

	def GetFunction(self):
		# Sets the Function for Fractal Generation (based on `self.GenType`)
		if self.GenType:
			self.MagicFunctionGenerator = GetFunction(self.GenType)
		else:
			raise ValueError("`self.GenType` is not Set!")

	def SetFunction(self, func):
		# Lets functions made by user be able to be used instead of prebuilt
		# This feature sucks unless you can write your own functions into a file

		self.MagicFunctionGenerator = lambda *args: (func(args[1]) - args[2])

	def ColorIn(self, b: float) -> tuple:
		# Function for returning a color
		return self.color.x(b)

	def Animate(self, frames, lMost = -1, rMost = 1, through="modulus"):
		# Function for Rendering Several Fractals Back to Back
		"""
		Rewrite this, this is such cool functionality but you wrote this like an idiot
		Make this into a separated module and just send the values of "self" to it
		"""

		if through == "rabbit":
			assert False # feature doesn't function and is therefore temporarily unavalible
			# Make Animation through values for [ SD R | TD R ]
			images = []
			mult = (rMost - lMost) / frames

			for frame in range(frames):
				images.append(self.eval(n = frame))

			# Variable for the Flat Images
			flat = [image[0] for image in images]

			if images[1]:
				# Variable for 3D images (ThreeDeeImage)
				TDI = [image[1] for image in images]
			else:
				TDI = None

			# Duration of 40 makes 25fps
			[ dataset[0].save( \
				f"{self.FileName} - {self.count}#{name}-gif.gif",
				save_all=True,
				append_images=[*dataset[0:], *dataset[-2:0:-1]],
				optimize=True, duration=40, loop=0
				)
				for dataset, name in [[flat, "flat"], [TDI, "TD"]] \
				if dataset
			]

		if through == "modulus":

			def MakeIMG(FileName: str, data: list):
				"""
				Function for image generation from data
				"""
				im = Image.new("RGBA", (self.SizeX, self.SizeY), (255, 255, 255, 255))
				pixel = im.load()
				for i in range(len(data)):
					for j in range(len(data[0])):
						pixel[j, self.SizeY - i - 1] = self.ColorIn(data[i][j])
				im.save(FileName)
				self.count += 1
				return im

			self.SizeY = int((self.BoxRange[0][1] / self.BoxRange[0][0]) * self.SizeX) # Gets Y Value of array
			images = [] # List of PIL Images that get generated
			mult = (rMost - lMost) / frames # value to muliply frame value to by to generate from Left-most to Right-most
			data = [] # List for where the data gets generated into
			for (oneline, _) in self.MakeFrame():
				"""
				Generates lines of the image and adds it to the `data` list
				"""
				data.append(oneline)

			for frame in range(frames):
				"""
				Goes through each frame
				"""
				FileName = f"{self.FileName} - #{self.count}.png" # Sets Filename
				if os.path.exists(FileName):
					"""
					Loads in images in case generation got interrupted and files that have been generated already exist
					"""
					images.append(Image.open(FileName))
					pu.InfoOut("[Load]:: {} / {} | {:.2f}%\t".format(frame, frames, 100 * (1 + frame) / frames), end="\r")
					self.count += 1
					continue
				self.color.ModulusValue = frame * mult + lMost
				images.append(MakeIMG(FileName, data))
				pu.InfoOut("[Frames]:: {} / {} | {:.2f}%\t".format(frame, frames, 100 * (1 + frame) / frames), end="\r")

			pu.InfoOut()

			# Variable for the Flat Images
			flat = [image for image in images]

			# Duration of 40 makes 25fps
			[ dataset[0].save( \
				f"{self.FileName} - {self.count}#{name}-gif.gif",
				save_all=True,
				append_images=[*dataset[0:], *dataset[-2:0:-1]],
				optimize=True, duration=40, loop=0
				)
				for dataset, name in [[flat, "flat"]] \
				if dataset
			]

		videoify(self.FileName).save()

	def TurtleSetup(self):
		"""
		Function for running interactive turtle window
		"""

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

	def GUI(self):
		"""
		Function for opening GUI interface for generator

		[ Coming Soon ]
		"""
		pass

	def close(self):		
		"""
		Function for Closing Turtle Window
		Should be changed to see if `self.win()` existed as well as to try and make sure that no other subprocesses continue to run. 
		"""
		self.win.bye()
		exit()
