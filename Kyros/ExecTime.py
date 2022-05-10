#!/usr/bin/env python3

import functools
import time

def ExecTime(func):

	# Wraps a function and prints execution time
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		Start = time.perf_counter()
		r = func(*args, **kwargs)
		print("Done in  {:.2f} Seconds".format(time.perf_counter() - Start))
		return r

	return wrapper