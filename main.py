#!/usr/bin/env python3

import Kyros

f = Kyros.fractal()
# f.FileName = "A --"
settings = {
	'count': 0,
	'ci': -0.6359321976472476,
	'cj': 0.08004012786314796,
	'IsJulia': False,
	'SizeX': 256,
	'MaxI': 1000,
	'RateOfColorChange': 9,
	'BoxRange': ((4, 4), (-2, -2)),
	'GenType': 'R TD',
	'ColorType': 'basic'
}

f.SetAll(settings = settings)
f.TD = 1
f.eval()


f.Animate(1000)
print("~~~FINISHED~~~")