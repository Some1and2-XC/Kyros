#!/usr/bin/env python3

from numba import jit

def GetFunction(GenType):
	if GenType == "SD TD":

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

	elif GenType == "R IT":
		@jit(nopython=True)
		def MagicFunctionGenerator(MaxI, cj, ci, zj, zi, v = 1):
			#Magic Generator Function  (b is the number of itterations)
			for b in range(MaxI):
				yout = zi * zj * 2 + ci - zj * v
				xout = zj ** 2 - zi ** 2 + cj - zi * v
				if yout * yout + xout * xout > 4:
					break
				zi = yout
				zj = xout
			return b

	elif GenType == "R TD":
		@jit(nopython=True)
		def MagicFunctionGenerator(MaxI, cj, ci, zj, zi, v = 1):
			#Magic Generator Function  (b is the number of itterations)
			DeltaDistance = 0
			r = 2
			for b in range(MaxI):
				yout = 2 * zi * zj + ci - zj * v
				xout = zj ** 2 - zi ** 2 + cj - zi * v
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

	elif GenType == "BS IT":

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

	elif GenType == "BS TD":

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

	elif GenType == "ABR IT":
		@jit(nopython=True)
		def MagicFunctionGenerator(MaxI, cj, ci, zj, zi, v = 1):
			#Magic Generator Function  (b is the number of itterations)
			for b in range(MaxI):
				yout = abs(2 * zi * zj) + ci - zj * v
				xout = zj ** 2 - zi ** 2 + cj - zi * v
				if yout * yout + xout * xout > 4:
					break
				zi = yout
				zj = xout
			return b

	elif GenType == "ABR TD":
		@jit(nopython=True)
		def MagicFunctionGenerator(MaxI, cj, ci, zj, zi, v = 1):
			#Magic Generator Function  (b is the number of itterations)
			DeltaDistance = 0
			r = 2
			for b in range(MaxI):
				yout = abs(2 * zi * zj) + ci - zj * v
				xout = zj ** 2 - zi ** 2 + cj - zi * v
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

	else: # SD IT
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

	return MagicFunctionGenerator