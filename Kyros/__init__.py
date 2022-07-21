#!/usr/bin/env python3

from PIL import Image

# Imports for File Information
import os
from random import randint

# Imports for Drawing to the Screen
import turtle

from math import cos, log2
from colorsys import hsv_to_rgb

from .functions import GetFunction
from .coloring import color
from .ThreeDeeify import TDObject
from .videoify import videoify
from .ExecTime import ExecTime

class fractal:

	def __init__(self):

		self.__version__ = "v0.0.0"
		self.line = "-" * 25
		self.ZoomAmnt = 2
		self.win = None

		# Used to specify wether the make Three Dee version
		self.TD = False

		# Makes File Name with Four Letters Between "A" and "Z" : ABCD.tx
		self.FileName = "F -- " + "".join( chr(randint(65, 90)) for i in range(4) )

		# Tries to make a directory with called `self.FileName`
		try:
			os.mkdir(self.FileName)
		except FileExistsError:
			# Exception Catch for if the folder that is attempted to be
			# created already exists
			...

		# Sets `self.FileName` to the folder that contains the files
		self.FileName = f"{self.FileName}\\{self.FileName}"

	@ExecTime
	def eval(self, turtle: bool = False, x: float = None, y: float = None, first = False, n = None):
		# Function that evaluates and draws graph

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

		self.PrintHeader()

		# Only Sets Data if it is going to be used to Generate a 3D version
		if self.TD:
			data = []

		# O(n) for memory usage
		# (for the variables defined, image data is still O(n^2) (Obvious reasons))

		for (oneline, i) in self.MakeFrame():
			if self.TD:
				data.append(oneline)
			for j in range(self.SizeX):
				pixel[j, self.SizeY - i - 1] = self.ColorIn(oneline[j])

		print(f"\n{self.line}")

		# Gets text added to the actual file that is Saved
		savedFile = f"{self.FileName} - #{self.count}.png"

		# Saves Image
		im.save(savedFile)

		if self.win:
			# Sets the background of the Turtle window as the newly created image
			self.win.bgpic(savedFile)

			# Updates the Turtle Screen
			self.win.update()

		# TDO is for `Three Dee Object`
		TDO = None
		if self.TD:
			# Sets TDO to the image data
			TDO = TDObject(f"{self.FileName} - {self.count}", data, self.ColorIn, self.MaxI, self.color.RateOfColorChange, n = self.count).eval()

		self.count += 1

		# Returns the two images that could potentially be generated from `self.eval()`
		return (im, TDO)

	def main(self, x: float = 0, y: float = 0, first: bool = False):
		# Main function for Running Turtles
		self.eval(turtle = True, x = x, y = y, first = first)
		return

	def PrintHeader(self, n = None):
		# Function for printing Header
		print(f"{self.__version__} - {self.FileName}#{self.count}\n{self.line}")
		return

	def SetAll(self, settings: dict = None, clr = None):
		# Defines all starting parameters

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

		return

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
			"colors = basic|sunset|ocean|fire",
			"",
			"Ex: ",
			"SD TD",
			"Makes Standard f(z) = z^2 | based on Travel Distance",
			""
		]

		genTxt = "\n".join(genTxt)

		genTxt += f"\n{self.color.ReturnText()}\n"

		genTxt += "\n" + " | ".join( \
			f"{text} : {str(value)}" for text, value in [ \

			["Name", self.FileName],
			["GenType", self.GenType],
			["TD Copy", self.TD]
		]
			if value
		)

		genTxt += f"\n{self.line}"

		with open(f"{self.FileName}.md", "a") as text:
			text.write(genTxt)

			text.close()

		return

	def WriteFileInformation(self):
		# Defines the text to add to the Image information file

		NameInfo = {
			"count": self.count,
			"ci": self.ci,
			"cj": self.cj,
			"IsJulia": self.IsJulia,
			"SizeX": self.SizeX,
			"MaxI": self.MaxI,
			"BoxRange": self.BoxRange,
			"GenType": self.GenType,
		}

		with open(f"{self.FileName}.md", "a") as text:
			text.write(f"\n{self.FileName}#{self.count} | {str(NameInfo)}")
			text.close()

		return True

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

	def MakeFrame(self):
		# Function for making each frame
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
			# Yield make the result of a function an itterator that only evaluates when is needed to (by something like a `for` loop)
			yield (line, i)
		if self.IsJulia is False:
			self.ci = self.cj = 0

	def ColorIn(self, b: float) -> tuple:
		# Function for returning a color
		return self.color.x(b)

	def Animate(self, frames, lMost = -1, rMost = 1, through="modulus"):
		# Function for Rendering Several Fractals Back to Back

		if through == "rabbit":
			assert False # feature doesn't function and is therefore temporarily unavalible
			# If the thing to animate through it rabbit
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
			images = []
			mult = (rMost - lMost) / frames

			for frame in range(frames):
				self.color.ModulusValue = frame * mult + lMost
				images.append(self.eval(n = frame))

			# Variable for the Flat Images
			flat = [image[0] for image in images]

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
		# Function for setting up turtle screen

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

	def OpenTurtleMenu(self):
		# Function for opening buttons as an overlay for turtle screen 
		1
		pass

	def close(self):
		# Function for Closing Turtles
		self.win.bye()
		exit()
