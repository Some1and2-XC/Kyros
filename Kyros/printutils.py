#!/usr/bin/env python3

"""
file for printing and writing information to files
"""

def InfoOut(string="", end="\n", sep=None):
	"""
	Function called by all other functions to specify what to do with the output
	# This is a seperate function because if a
	   different way of showing output is
	   wanted (such as logging instead of just printing)
	   this function can be just changed
	"""

	print(string, end=end, sep=sep)

def line():
	"""
	# Prints a line
	"""

	print("-" * 25)

def PrintHeader(version, FileName, count):
	"""
	Function for printing Header
	version  :: version of program
	FileName :: Name of the file being saved
	count    :: which item is being generated
	"""

	print(f"{version} - {FileName}#{count}")
	line()

def WriteFileInformation(FileName, count, ci, cj, IsJulia, SizeX, MaxI, BoxRange, GenType):
	"""
	Function for writing the file

	FileName :: The name of the file that is to be written to (no file extension)
	count    :: The Index of image that has been generated
	ci       :: constant `I` (imaginary) value for JuliaSet generation
	cj       :: constant `J` (real) value for JuliaSet generation
	IsJulia  :: Bool of if the set is a juliaset
	SizeX    :: The amount of pixels in the X Direction
	MaxI     :: Maximum Amount of itterations for generation
	BoxRange :: tuple of tuples of mathematical information
				   (see `kyros.fractal().eval()` `if not first:` line for more information)
	GenType  :: Generation Function used
	"""

	NameInfo = {
		"count": count,
		"ci": ci,
		"cj": cj,
		"IsJulia": IsJulia,
		"SizeX": SizeX,
		"MaxI": MaxI,
		"BoxRange": BoxRange,
		"GenType": GenType,
	}

	with open(f"{FileName}.md", "a") as text:
		text.write(f"\n{FileName}#{count} | {str(NameInfo)}")
		text.close()

