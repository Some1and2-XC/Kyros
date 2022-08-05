#!/usr/bin/env python3

# `f` is for `fractal` & `c` is for `color`

from . import fractal, color

f = fractal(FileName = "F -- ZHQQ")

MaxI = 500

c = color(
	RateOfColorChange = 9,
	MaxI = 10000,
	ColorStyle = "rotational",
	ShadowStyle = "modulus"
	# ShadowStyle = "none"
)

c.ModulusValue = 3

settings = {
	"count": 0,
	'ci': 0,
	'cj': 0,
	"MaxI": 1000,
	"IsJulia": False,
	"SizeX": 2048,
	"RateOfColorChange": 9,
	"BoxRange": ((0.027777777777777776, 0.015625), (-1.4044444444444442, 0.0007506672597865048)),
	"GenType": "SD TD"
}


f.SetAll(settings = settings, clr = c)

# f.TD = True

# f.eval()

# f.TurtleSetup()

f.Animate(1000, lMost = 10, rMost = 50, through = "modulus")

input(f"\n{f.FileName}\n\t~~~FINISHED~~~")