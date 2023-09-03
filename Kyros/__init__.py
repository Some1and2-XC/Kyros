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

		def GetRandomFileName(FileNamePrefix: str = "F -- ", FileNameLength: int = 4):
			"""
			Function for setting a random filename if none is supplied

			FileNamePrefix :: The first few characters from a filename to be generated
			FileNameLength :: Length of the filename to be returned
			"""

			from random import randint

			return FileNamePrefix + "".join( \
				chr(randint(65, 90))\
				for i in range(FileNameLength)
			)

		# Initial Settings
		self.__version__ = "v0.0.0"
		self.line = "-" * 25
		self.TD = False # Used to specify wether the make 3D version

		# Turtle Settings
		self.ZoomAmnt = 2 # The amount that the image zooms each click (with turtle / web version)
		self.win = None # window variable for turtle

		# Sets filename based on `GetRandomFileName()` function if `FileName` isn't passed to `__init__()``
		if FileName: self.FileName = FileName
		else: self.FileName = GetRandomFileName()

		# Tries to make a directory for putting files into
		try: os.mkdir(self.FileName) # Tries to make a directory with called `self.FileName`
		except FileExistsError: ...  # If the file already exists, do nothing

		# Sets `self.FileName` to the folder that contains the files
		self.FileName = os.path.join(self.FileName, self.FileName)

	@ExecTime
	def eval(self, x: float = None, y: float = None, first = True) -> tuple:

		"""
		Function for evaluating the settings of the fractal
		& saving the image

		x     :: x value for where the image is desired to be generated (in mathematical space)
		y     :: y value for where the image is desired to be generated (in mathematical space)
		first :: Flag Specifying wether or not the file that is being generated from `eval` is the first image being generated

		returns -> tuple :: (2D_Imagedata, 3D_Imagedata)
		###### (Returns only (2D_Imagedata, None) if `self.TD` is set to False)
		"""

		def GetInitialValues():
			"""
			Sets some initial values for generation
			"""

			self.SizeY = int((self.BoxRange[0][1] / self.BoxRange[0][0]) * self.SizeX) # Sets SizeY based on what SizeX is
			if not first:
				"""
				If the image is not the first image generated in a series (if modification to where the image exists is required. )
				"""
				ClickLocation = (2 * x / self.SizeX, 2 * y / self.SizeY) # Finds which percentage of the screen was "Clicked" on
				self.BoxRange = (
					(
						self.BoxRange[0][0] / self.ZoomAmnt, # Sets Math X length value (distance between left and right)
						self.BoxRange[0][1] / self.ZoomAmnt  # Sets Math Y length value (distance between bottom and top)
					), 
					(
						self.BoxRange[1][0] + (self.BoxRange[0][0] - (self.BoxRange[0][0] / self.ZoomAmnt)) / 2 + self.BoxRange[0][0] * ClickLocation[0] / self.ZoomAmnt, # Sets the Math leftmost value
						self.BoxRange[1][1] + (self.BoxRange[0][1] - (self.BoxRange[0][1] / self.ZoomAmnt)) / 2 + self.BoxRange[0][1] * ClickLocation[1] / self.ZoomAmnt  # Sets the Math bottomost value
					)
				) # BoxRange is the mathematical coordinates that define where the shape exists, in this case changing it based on ClickLocation
			return True
		
		def PutInitialInformation():
			"""
			Function for writing information (generally to console)
			"""
			pu.WriteFileInformation(self.FileName, self.count, self.ci, self.cj, self.IsJulia, self.SizeX, self.MaxI, self.BoxRange, self.GenType) # Prints file information
			pu.PrintHeader(self.__version__, self.FileName, self.count) # Prints some header information
		
		def RunMath():
			"""
			Function for Running math and saving image data
			"""
			if self.TD:
				"""
				If the Flag for defining wether or not to generate 3D Version is True, make a duplicate of `self.MakeFrame()` to send to `TDObeject()`
				"""
				data = [i for i in self.MakeFrame()] # Sets the `data` variable to be the output of `self.MakeFrame()`
				im.putdata( [ self.ColorIn(i) for i in data ] )

				# The dimension of the array has to be resized to make sure that the `TDObject().eval()` gets the right kind of data
				outdata = []
				for i in range(self.SizeY):
					outdata.append([])
					for j in range(self.SizeX):
						outdata[i].append(data[i * self.SizeX + j])

				# The problem is probably caused by the fact that you are passing in "data" which has been converted to its `self.ColorIn(i)` of `for i in self.MakeFrame()`
				TDO = TDObject(f"{self.FileName} - {self.count}", outdata, self.ColorIn, self.MaxI, n = self.count).eval()

			else:
				data = [ self.ColorIn(i) for i in self.MakeFrame() ]
				im.putdata( data ) # because TD is False, the program doesn't have to save the data as the `data` variable, instead extract the values of the data directly into the image. 

		def TryLoadData():
			"""
			Function for opening pickle data for a semi completed file
			"""

			import pickle

			try:
				with open(f"{self.FileName}.pkl", "rb") as outfile:
					...
			except:
				...

		def SaveInbetweenData():
			"""
			Function for pickling the image data
			"""

			import pickle

			with open(f"{self.FileName}.pkl", "wb") as outfile:
				pickle.dump(im)
				pickle.dump(i)
				pickle.dump(j - 1)

		def PutEndInformation():
			"""
			Writes the information about file generation
			"""
			pu.InfoOut() # Prints Space
			pu.line() # Prints Line

		def UpdateTurtle():
			"""
			Function for setting the background image of the turtle window to be the generated image 
			"""
			self.win.bgpic(SavedFile)
			self.win.update()

		# Sets Required Variables
		TDO = None # Sets the initial value of TDO so that if self.TD is not True, the function still returns something
		SavedFile = f"{self.FileName} - #{self.count}.png" # Sets Filename to save to

		GetInitialValues()
		im = Image.new("RGBA", (self.SizeX, self.SizeY), (255, 255, 255, 255)) # Makes new PIL object with a background color of (255, 255, 255, 255)
		PutInitialInformation()

		try: RunMath()
		except KeyboardInterrupt:
			"""
			In case user wants to ctrl-z out of the program durring execution
			"""

		PutEndInformation()

		im.save(fp = SavedFile) # Saves Image (fp is file path)
		if self.win: UpdateTurtle()
		self.count += 1 # Incremements the counter for the amount of images that have been generated
		return (im, TDO) # Returns the data of the two images that could be generated from `self.eval()`

	def MakeFrame(self):
		"""
		Function for generating each frame
		Returns a generator that only evaluates the math when it is necessary
		yields a value based on MagicFunctionGenerator
		reduces the need for having a massive amount of data being store redundantly in mulitple arrays. 
		"""

		global PixelIteratorI, PixelIteratorJ

		for PixelIteratorI in range(int(self.SizeY + .5)): # Goes through each horizontal line
			for PixelIteratorJ in range(self.SizeX): # Goes through each pixel in the line
				# Gets Generator Values based on relative position of BoxRange
				# Adjusts values based on if the IsJulia flag is set. 
				if self.IsJulia is False:
					self.ci = PixelIteratorI * self.BoxRange[0][1] / (self.SizeY - 1) + self.BoxRange[1][1]
					self.cj = PixelIteratorJ * self.BoxRange[0][0] / (self.SizeX - 1) + self.BoxRange[1][0]
					zi = 0
					zj = 0
				if self.IsJulia is True:
					zi = PixelIteratorI * self.BoxRange[0][1] / (self.SizeY - 1) + self.BoxRange[1][1]
					zj = PixelIteratorJ * self.BoxRange[0][0] / (self.SizeX - 1) + self.BoxRange[1][0]
				
				# Sends variables to Magic Generator Function
				yield self.MagicFunctionGenerator(self.MaxI, self.cj, self.ci, zj, zi)

			# Prints progress bar
			pu.InfoOut("{spaces}{CurrentWorkingNumber} / {TotalNumber} | {percentage:.2f}%".format(
					spaces               = " " * (len(str(self.SizeY)) - len(str(PixelIteratorI + 1))),
					CurrentWorkingNumber = PixelIteratorI + 1,
					TotalNumber          = self.SizeY,
					percentage           = 100 * (PixelIteratorI + 1) / self.SizeY
				),
				end="\r"
			)
		if self.IsJulia is False: self.ci = self.cj = 0

	def SetAll(self, settings: dict = None, clr = None):
		# Defines all starting parameters
		"""
		Defines all Starting Parameters

		settings :: a dictionary of all the settings to be passed to the generator
		clr      :: a `color` object that has all the parameters set to be able to create color generation settings
		"""

		if settings is None:
			settings = {
				"count"    : 0,
				"ci"       : 0,
				"cj"       : 0,
				"IsJulia"  : False,
				"SizeX"    : 512,
				"MaxI"     : 1000,
				"BoxRange" : ((4, 4), (-2, -2)),
				"GenType"  : "SD IT"
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
		"""
		Function for writing header information to data output file
		"""
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
		"""
		Function for getting a color value from `b`
		"""
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

		RunFromTurtle = lambda x, y : self.eval(x = x, y = - y, first = False) # Sets in between function for the turtle window to call `onclick`

		# Sets up turtle screen to Match the file Generated Ratio
		self.win = turtle.Screen() # Initializes turtle screen
		self.win.setup(self.SizeX, int((self.BoxRange[0][1] / self.BoxRange[0][0]) * self.SizeX)) # Sets up values for turtle screen
		self.win.tracer(0, 0) # Makes it so that the window doesn't do auto refereshes
		self.win.title(f"{self.__version__} - {self.FileName}") # Sets the title of the window. 

		# Makes any key that is pressed close the window
		self.win.listen() # Makes the window listen for key strokes
		for i in range(35, 127): # Goes through a list of letters and makes the window close if any of them are pressed
			self.win.onkeypress(self.close, chr(i))

		self.eval(first = True) # Calls the main function to generate the first image
		self.win.onclick(RunFromTurtle)
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


