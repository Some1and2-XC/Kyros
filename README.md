# Some1and2's Kyros - A Fractal Generator
#### Basic Class Oriented Fractal Generator with Binary Single Threaded Acceleration made with python
# Key Features:: 
 - Uses Compiler Optimisation for faster Execution Time
 - Functionality for Various kinds of Fractals such as the `Mandelbrot`, `Julia` & `Burning Ship` fractals (and more)
 - Various Color Pallets for assigning Colors to Values
 - Generates an information file from Generator Data
    - Includes the Settings used to so that the image can be Regenerated with tweaked settings
 - Support for making 3D versions of `fractals`
    - Uses Orthographic Projection for rendering in 3D
 - Added ability to export series of sets as `.mp4` video files
    - Uses optional `.dll` file to save `.mp4` files with the HVEC 264 codec for Better compression without loss of quality

# Basic Usage::

### For Quick Testing [running just the `__main__.py`]
```python
py -m Kyros
```

### Setup
```python
import Kyros

f = Kyros.fractal()
```

### For Setting Parameters
```python
 # Function for Setting all the data at once to Preset Settings
f.SetAll()

 # To make a 3D Version of a graph, set the `TD` variable to `True`
f.TD = True
```

### For Evaluating the Function
```python
 # Function that evaluates and saves the Function as an image
f.eval()

 # Function that opens a Turtle Window as a Display
f.TurtleSetup()
```

## For Evaluating the Function as a Video
```python
f.Animate(frames = 1000, )
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