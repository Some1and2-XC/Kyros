#!/usr/bin/env python3

# `f` is for `fractal` & `c` is for `color`

from . import fractal, color

f = fractal()

MaxI = 1000

c = color(
	RateOfColorChange = 9,
	MaxI = MaxI,
	ColorStyle = "rotational",
	ShadowStyle = "modulus"
)

c.ModulusValue = 3

settings = {
	"count": 0,
	'ci': -0.6359321976472476,
	'cj': 0.08004012786314796,
	"IsJulia": True,
	"SizeX": 512,
	"MaxI": 500,
	"BoxRange":((0.5, 0.5), (-0.22265625, 0.19921875)),
	"GenType": "SD TD",
}


f.SetAll(settings = settings, clr = c)

f.TD = True

f.eval()

# f.Animate(1000, lMost = 1, rMost = 10, through = "modulus")

print(f"\n{f.FileName}\n	~~~FINISHED~~~")

input()