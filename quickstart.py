#!/usr/bin/env python3

from Kyros import fractal, color

f = fractal(FileName = None)

MaxI = 50

c = color(
	RateOfColorChange = 9,
	MaxI = MaxI,
	# ColorName = "sunset",
	ColorStyle = "rotational",
	ShadowStyle = "none"
)
c.ModulusValue = 3

settings = {
	"count": 0,
	"ci": -0.6359321976472476,
	"cj": 0.08004012786314796,
	"IsJulia": False,
	"SizeX": 1280,
	"MaxI": MaxI,
	"RateOfColorChange": 9,
	# "BoxRange": ((0.00086806, 0.00043403), (-0.09848914930555545, 0.6495883493661031)),
	"BoxRange": ((4, 4), (-2, -2)),
	"GenType": "ABR IT"
}

f.SetAll(settings = settings, clr = c)
f.eval()

input(f"\n{f.FileName}\n\t~~~FINISHED~~~")
