#!/usr/bin/env python3

# `f` is for `fractal` & `c` is for `color`

from . import fractal, color

f = fractal()

MaxI = 500

c = color(
	RateOfColorChange = 9,
	MaxI = MaxI,
	ColorStyle = "rotational",
	ShadowStyle = "modulus"
)

c.ModulusValue = 3

settings = {
	"count": 0,
	'ci': 0,
	'cj': 0,
	"MaxI": MaxI,
	"IsJulia": False,
	"SizeX": 512,
	"RateOfColorChange": 9,
	# "BoxRange": ((0.00086806, 0.00043403), (-0.09848914930555545, 0.6495883493661031)),
	"BoxRange": ((4, 4), (-2, -2)),
	"GenType": "SD TD"
}


f.SetAll(settings = settings, clr = c)

# f.TD = True

# f.eval()

f.TurtleSetup()

# f.Animate(1000, lMost = 1, rMost = 10, through = "modulus")

input(f"\n{f.FileName}\n	~~~FINISHED~~~")