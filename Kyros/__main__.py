#!/usr/bin/env python3

# `f` is for `fractal` & `c` is for `color`

from . import fractal, color


# from os import chdir; chdir(r"E:\.py\Fractals\Kyros\Best Version v0.0.0 Current Development")

f = fractal(FileName = "Test")

MaxI = 1000

c = color(
	RateOfColorChange = 9,
	# MaxI = MaxI,
	MaxI = 1000,
	ColorStyle = "rotational",
	ShadowStyle = "none"
	# ShadowStyle = "none"
)

c.ModulusValue = 3

settings = {
	"count": 0,
	'ci': 0,
	'cj': 0,
	"MaxI": MaxI,
	"IsJulia": False,
	"SizeX": 1024,
	"BoxRange": ((4, 4), (-2, -2)),
	"GenType": "SD IT"
}


f.SetAll(settings = settings, clr = c)
# f.TD = True
f.eval()

# f.TurtleSetup()
# f.Animate(1000, lMost = 10, rMost = 50, through = "modulus")

input(f"\n{f.FileName}\n\t~~~FINISHED~~~")