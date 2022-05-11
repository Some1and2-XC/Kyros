#!/usr/bin/env python3

from PIL import Image
from numba import jit

# google how to make graficcx
# realize girafic'x don't exist
# My life is a lie

# Make the camera lense ajustable later

def str2lst(data):
	data = data.split("]")[:-2]
	data = [ [float(j) for j in i[3:].split(", ")] for i in data ]
	return data


def CubicTriangleAssembly(data):
	global yHeightMultiplyer, MaxI, ColorType, RateOfColorChange

	for i in range(len(data) - 1):
		for j in range(len(data[i]) - 1):
			if data[i][j] != 0:
				# more gamer coding
				yield {
				"data":((i, j, data[i][j] * yHeightMultiplyer), (i+1, j, data[i+1][j] * yHeightMultiplyer), (i, j+1, data[i][j+1] * yHeightMultiplyer)),
				"color": get.ColorIn(data[i][j], MaxI, RateOfColorChange, ColorType)
				}

				yield {
				"data":((i+1, j+1, data[i+1][j+1] * yHeightMultiplyer), (i, j+1, data[i][j+1] * yHeightMultiplyer), (i+1, j, data[i+1][j] * yHeightMultiplyer)),
				"color": get.ColorIn(data[i][j], MaxI, RateOfColorChange, ColorType)
				}
	return


def SquaredTriangleAssembly(data, x, y):
	# Takes the info fram CubicTriangleAssembly then transforms into 2D linear equations for boundries of triangles
	# Makes 2D Triangles out of 3D array
	return [{"data": TransformFunc(i["data"]), "color": i["color"]} for i in data][::-1]


def TransformFunc(triuple):
	global xLen
	# Just cosine of 30 degrees
	cosN = 0.866025403784
	sinN = 0.5
	# (i, j, index) = triuple

	responces = []
	for n in triuple:
		# responces.append((j - i + xLen) * .5, (j * sinN + i * sinN + index) / (cosN * 2))
		responces.append(((n[1] - n[0] + xLen) * .5, (n[1] * sinN + n[0] * sinN + n[2]) / (cosN * 2)))
	return tuple(responces)


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


@jit(nopython=True)
def IsBetween(A, B, C, x, y):
	# Sees if C is on the same side of A and B as the point (x, y)
	# m & b variables are variables used in y = mx + b
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


def GetBox(data):
	# Returns a list of the bottom left + top right of the triangle
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


# def IsInDirection(data):


def ObjectArrayCreate(data: list, name: str, info: tuple):
	global MaxI, xLen, yLen, yHeightMultiplyer, BackgroundColor, ColorType, RateOfColorChange
	(MaxI, ColorType, RateOfColorChange) = info
	del info

	# Actual Dimensions of end Image
	imX = int(1024 * 8)
	imY = int(imX * 9 / 16)

	# Dimensions of the list supplied
	xLen = len(data)
	yLen = len(data[0])

	yHeightMultiplyer = 0.5 * xLen / MaxI

	# Get the actual relative screen location for the data points?
	# This splits the data into sets of 3 triangles 

	print("Starting 3D Process...")
	
	data = CubicTriangleAssembly(data)
	print("Cubic Triangle Assembly Complete!")
	# Data becomes list of triangle corners with coordinates
	data = SquaredTriangleAssembly(data, xLen, yLen)
	print("Squared Triangle Assembly Complete!")

	print("-" * 25)

	BackgroundColor = (255, 255, 255, 0)
	im = Image.new("RGBA", (imX, imY), BackgroundColor)
	pixel = im.load()

	for i in range(len(data)):
		print(f"{i + 1} / {len(data)} | {100 * (i + 1) / len(data):.2f}%   ", end="\r")
		i = data[i]

		# Gets the extreme corners of a triangle to find a box to search for pixels within
		Box = GetBox(i["data"])

		# Number to multiply the Box values by
		Mult = [imX / xLen, imY / yLen]

		Box = [ [ int(Box[i][j] * Mult[j]) for j in range(2) ] for i in range(2) ]

		del Mult

		# Adding one to each range so that the last pixel found in 'Box' is searched
		for j in range(Box[0][0], Box[1][0] + 1):
			# makes sure j is in range
			if 0 < j <= imX:
				for k in range(Box[0][1], Box[1][1] + 1):
					# makes sure k is in range
					if 0 < k <= imY:
						# IsInATriangle() returns [bool, ColorValue] which is why if statement looks for n[0]
						n = IsInATriangle(i, (j * xLen / imX, k * yLen / imY))
						if n[0]:
							try:
								if 0 <= imY - k - 1 < imY:
									# Sets Pixel to the color of n[1] which is the color value
									pixel[j, imY - k - 1] = n[1]
							except:
								1
	im.save(f"{name}-3D.png")
	print()
	print("-" * 25)
	return im
