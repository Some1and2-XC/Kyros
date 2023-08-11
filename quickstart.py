#!/usr/bin/env python3

from Kyros import fractal, color

f = fractal(FileName = None)

MaxI = 500

c = color(
	RateOfColorChange = 9,
	MaxI = MaxI,
        ColorName = "sunset",
	ColorStyle = "sinusoidal",
	ShadowStyle = "none"
)
c.ModulusValue = 3

settings = {
	"count": 0,
	"ci": 0,
	"cj": 0,
	"IsJulia": False,
	"SizeX": 1280,
	"MaxI": MaxI,
	"RateOfColorChange": 9,
	"BoxRange": ((0.00086806, 0.00043403), (-0.09848914930555545, 0.6495883493661031)),
	"GenType": "SD TD"
}

f.SetAll(settings = settings, clr = c)
f.eval()

input(f"\n{f.FileName}\n\t~~~FINISHED~~~")
