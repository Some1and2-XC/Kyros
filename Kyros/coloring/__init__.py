#!/usr/bin/env python3

from colorsys import hsv_to_rgb
from math import cos

class color:

	"""
	Class for coloring Kyros Fractals
	"""

	def __init__(self, RateOfColorChange: int, MaxI: int = None, ColorStyle: str = "rotational", ShadowStyle: str = "none", MaxValue: int = 0, MinValue: int = 0, ColorName: str = ""):
		"""
		`__init__()` function for the `color` class
		`name`" is optional
		`MaxI` is only optional because the fact that the color module is class based means that the
		color can be set after the initial class is defined
		"""

		self.ColorStyle = ColorStyle
		self.ShadowStyle = ShadowStyle

		# Initialisation

		NameDefinitions = {"sunset": (277, 420), "ocean": (14, 25), "fire": (-40, 65), "red": (-20, 25)}
		PossibleColorStyles = {"rotational", "sinusoidal"}
		PossibleShadowStyles = {"none", "minimal", "modulus"}

		if ColorStyle not in PossibleColorStyles:
			raise ValueError(f"`{ColorStyle}` not in  `PossibleColorStyles`")
		if ShadowStyle not in PossibleShadowStyles:
			raise ValueError(f"`{ShadowStyle}` not in  `PossibleShadowStyles`")

		# Setting `self` Attributes

		if ColorName in NameDefinitions:
			(self.MaxValue, self.MinValue) = NameDefinitions[ColorName]
			self.ColorName = ColorName
		else:
			self.MaxValue = MaxValue
			self.MinValue = MinValue
		self.RateOfColorChange = RateOfColorChange
		self.MaxI = MaxI

		# Setting `self.BetweenColorFunction()` & `self.BetweenShadowFunction()`
		# `self.BetweenColorFuction()` is the Function for between `x()` and the value

		def ToRadians(n):
			# Function that takes a degree value and returns it in radians
			return n * 3.141592653589792323 / 180

		
		if ColorStyle == "rotational":
			def BetweenColorFunction(b):
				hue = b * self.RateOfColorChange
				return hue

		if ColorStyle == "sinusoidal":
			def BetweenColorFunction(b):
				if not (self.MaxValue and self.MinValue):
					raise ValueError("`self.MinValue` / `self.MaxValue` Not Set!")

				hue = ((self.MaxValue - self.MinValue) * .5 * cos(ToRadians(b * self.RateOfColorChange))
					+ (self.MaxValue + self.MinValue) * .5) % 360
				return hue

		if ShadowStyle == "none":
			def BetweenShadowFunction(b):
				value = 1
				return value

		if ShadowStyle == "minimal":
			def BetweenShadowFunction(b):
				value =  .125 * cos(ToRadians(b * self.RateOfColorChange)) + .815
				return value

		if ShadowStyle == "modulus":
			self.ModulusValue = None
			def BetweenShadowFunction(b):
				if not self.ModulusValue:
					raise ValueError("`self.ModulusValue` Not Set!")
				def r(x):
					# function that will decide how dark the result is every itteration
					return 1 / (x + 1)
				# Amount of itterations until it cycles
				if self.ModulusValue is not None:
					n = self.ModulusValue
				else:
					n = 10 # for frame 1 if lMost=10
				value = 1 - (r(b % n) - r(0)) / (r(n) - r(0))
				return value

		self.BetweenColorFunction = BetweenColorFunction
		self.BetweenShadowFunction = BetweenShadowFunction

	def x(self, b):
		# Function that returns color based on Previous settings an `b` value

		if b == 0:
			# Returns a transparent if i == 0
			return (255, 255, 255, 255)

		if b >= (self.MaxI) - 1:
			# Returns Black if the Maximum value is the `b` value
			return (0, 0, 0, 255)

		hue = self.BetweenColorFunction(b)
		value = self.BetweenShadowFunction(b)

		return tuple(int(i * 255) for i in (*hsv_to_rgb(hue / 360, 1, value), 1))

	def ReturnText(self):
		# Function for returning text for writing to file

		Attributes = self.__dict__

		# Me just discovering you can use `list` comprehension in dictionaries
		# Basically Removes the functions from the listed attributes
		# Goes Through the attribute list and if if the type of data at each attribute is not the same type as `lambda:None` (a lambda function that takes no input and returns `None`)
		# Then that attribute gets added
		Attributes = {i: Attributes[i] for i in Attributes if type(Attributes[i]) != type(lambda:None)}

		return f"Color Settings : {Attributes}"
