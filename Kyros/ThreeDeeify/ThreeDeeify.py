#!/usr/bin/env python3

from PIL import Image
from numba import jit

from math import log2

class TDObject:
	def __init__(
		self, name: str,  data, ColorFunc, MaxI, ColorType, RateOfColorChange, imX = 1024, n: int = None):
		self.name = name
		self.data = data
		self.ColorFunc = ColorFunc
		self.MaxI = MaxI
		self.ColorType = ColorType
		self.RateOfColorChange = RateOfColorChange

		self.n = n

		self.imX = int(imX) # Be default is set to 1024

	# Function for evaluating
	def eval(self):

		# Actual Dimensions of end Image
		self.imY = int(self.imX * 9 / 16)

		# Dimensions of the list supplied
		self.xLen = len(self.data)
		self.yLen = len(self.data[0])

		self.yHeightMultiplyer = 2 ** 0 * (self.yLen / Logify(self.MaxI))

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

		BackgroundColor = (255, 255, 255, 255)
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
		self.name
		if self.n is not None:
			self.name += f"#{self.n}"
		im.save(f"{self.name} - 3D.png")
		print()
		print("-" * 25)

		return im

	# Function for formatting the data such that the triangles are accessable to the other functions, makes `data` into a list of triangles in 3D space
	def CubicTriangleAssembly(self):
		for i in range(self.xLen - 1):
			for j in range(self.yLen - 1):
				if self.data[i][j] != 0:
					# more gamer coding
					if self.data[i][j] != 0 and self.data[i+1][j] != 0 and self.data[i][j+1] != 0 or True:
							yield {
								"data":((i, j, Logify(self.data[i][j]) * self.yHeightMultiplyer), (i+1, j, Logify(self.data[i+1][j]) * self.yHeightMultiplyer), (i, j+1, Logify(self.data[i][j+1]) * self.yHeightMultiplyer)),
								"color": self.ColorFunc(self.data[i][j])
							}
					if self.data[i+1][j+1] != 0 and self.data[i+1][j] != 0 and self.data[i][j+1] != 0 or True:
							yield {
								"data":((i+1, j+1, Logify(self.data[i+1][j+1]) * self.yHeightMultiplyer), (i, j+1, Logify(self.data[i][j+1]) * self.yHeightMultiplyer), (i+1, j, Logify(self.data[i+1][j]) * self.yHeightMultiplyer)),
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

def Logify(n: float) -> float:
	if n == 0:
		return 0
	else:
		return log2(n)