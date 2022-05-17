# Some1and2's Kyros - A Fractal Generator
#### Basic Class Oriented Fractal Generator with Binary Acceleration - Single Threaded, made with python
# Key Features:: 
 - Uses CPU Optimisation for faster Execution Time
 - Functionality for Various kinds of Fractals such as the `Mandelbrot`, `Julia` & `Burning Ship` fractals (and more)
 - Various Color Pallets for the Generators
 - Output File for Generator Data, Saves the Settings used to an Output file so that the settings can be Reused and Images can be Recreated at Higher Resolution etc
 - Support for making 3D versions of `fractals`

# Basic Usage::
```python
import Kyros

f = Kyros.fractal()

 # Function for Setting all the data at once to Preset Settings
f.SetAll()

 # Function for Getting Data through Text Box Input
f.GetData()

 # To make a 3D Version of a graph, set the `TD` variable to `True`
f.TD = True

 # Function for setting the function used by Kyros [Very Optional]
f.SetFunction(func=function)

 # Function that evaluates and saves the Graph
f.eval()

 # Function that opens a Turtle Window as a Display
f.TurtleSetup()

```

# Installation::
#### From PIP:
```bat
pip install Kyros
```

#### From GITHUB: 
```bat
pip install wheel
cd __directory__
py setup.py bdist_wheel
pip install dist\__version__
```

# Test::
#### To Make a Copy of the `Social preview` of the Library:
```python
import Kyros

settings = {
	"count": 0,
	"ci": 0,
	"cj": 0,
	"IsJulia": False,
	"SizeX": 1280,
	"MaxI": 500,
	"RateOfColorChange": 9,
	"BoxRange": ((0.00086806, 0.00043403), (-0.09848914930555545, 0.6495883493661031)),
	"GenType": "SD TD",
	"ColorType": "sunset"
}

f = Kyros.fractal()
f.SetAll(settings)
f.TurtleSetup()
```

# Current Work::
### See `TODO.md` to see what is being worked

---
**Documentation** *[Coming Soon]*