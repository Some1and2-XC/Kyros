#!/usr/bin/env python3

# `f` is for `fractal` & `c` is for `color`

from . import fractal, color

f = fractal(FileName = None)

MaxI = 500

c = color(
	RateOfColorChange = 9,
	MaxI = MaxI,
	ColorStyle = "rotational",
	ShadowStyle = "modulus"
	# ShadowStyle = "none"
)

c.ModulusValue = 3

settings = {
	"count": 0,
	'ci': 0,
	'cj': 0,
	"MaxI": MaxI,
	"IsJulia": False,
	"SizeX": 4096,
	"BoxRange": ((4, 4), (-2, -2)),
	"GenType": "SD TD"
}


f.SetAll(settings = settings, clr = c)

# f.TD = True

f.eval()

# f.TurtleSetup()

# f.Animate(1000, lMost = 10, rMost = 50, through = "modulus")

input(f"\n{f.FileName}\n\t~~~FINISHED~~~")