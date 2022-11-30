#!/usr/bin/env python3

# `f` is for `fractal` & `c` is for `color`

from . import fractal, color

# from os import chdir; chdir(r"E:\.py\Fractals\Kyros\Best Version v0.0.0 Current Development")

f = fractal(FileName = "130k SD-TD")
# f = fractal()

MaxI = 1000

c = color(
	RateOfColorChange = 9,
	MaxI = MaxI,
	ColorStyle = "rotational",
	ShadowStyle = "none"
)

c.ModulusValue = 3

settings = {
	"count"    : 0,
	"cj" : 0.08004012786314796,
	"ci" :  - 0.6359321976472476,
	"MaxI"     : MaxI,
	"IsJulia"  : True,
	"SizeX"    : 1024,
	"BoxRange" : ((4, 4), (-2, -2)),
	"GenType"  : "SD TD"
}


f.SetAll(settings = settings, clr = c)
# f.TD = True
f.eval()

# f.TurtleSetup()
# f.Animate(1000, lMost = 10, rMost = 50, through = "modulus")

input(f"\n{f.FileName}\n\t~~~FINISHED~~~")