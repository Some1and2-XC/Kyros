<h1>
	<img src="https://github.com/Some1and2-XC/Kyros/assets/89313812/5ae3c003-1f34-4130-b46f-9715e105d03b" width="200em">
 	 - A Fractal Generator
</h1>

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

### For Quick Testing [running just the `__main__.py` file]
```python
py -m Kyros
```

### Setup
 - Initialises the Fractal Object
```python
import Kyros

f = Kyros.fractal()
```

### For Setting Parameters
 - Settings Basic Parameters
```python
 # Function for Setting all the data at once to Preset Settings
f.SetAll()

 # To make a 3D Version of a graph, set the `TD` variable to `True`
f.TD = True
```

### For Evaluating the Function
 - To Evaluate the Funcion set after all the Required Settings are Set
```python
 # Function that evaluates and saves the Function as an image
f.eval()

 # Function that opens a Turtle Window as a Display
f.TurtleSetup()
```

### For Evaluating the Function as a Video
 - To make a video from the fractal, use the `Kyros.fractal.Animate()` function
 - Set the amount of frames as well as the style of Video Created
```python
f.Animate(frames = 1000, through = "modulus")
```

# Setting Settings
### General Settings
 - For settings custom settings you must first make a Python Dictionary with all the required settings
```python
settings = {
	"count": "The Index of the image",

	"ci": "The constant Imaginary Value for Julia Sets",

	"cj": "The Constant Real Value for Julia Sets",

	"IsJulia": "Specifies wether the Generation is for a Julia set or not",

	"SizeX": "The Amount of pixels in the `x` direction",

	"MaxI": "The Maximum Amount of Itterations for the Render",

	"BoxRange": "Tuple of Tuples for the location of where the Generator is referencing from\
		the first tuple is the (x, y) values of the distance\
		the second tuple is for the (x, y) coordinates of the bottom left of the image",

	"GenType": "The Type of Generator Selected"
}
```

### Color Settings
 - The color generation Settings must also be set seperately from the image generation settings
 - The color however isn't set through a settings dictionary, instead being set through its own `Kyros.color` class

```python
import Kyros

c = Kyros.color(
	RateOfColorChange = "The Amount of Degrees the Colors Change per\
		itteration for Rotational Color",

	MaxI = "The value of the Maximum Amount of Itterations",

	ColorStyle = "The Style of Color Generation - Must be {'rotational', 'sinusoidal'}",

	ShadowStyle = "The Style of Shadow Generation - Must be {'none', 'minimal', 'modulus'}\
		If this is set to `modulus`, the attribute `.ModulusValue` must also be set to the color class",

	MaxValue = "For `sinusoidal` color there must be a minimum & Maximum\
		value for which the the color goes between",

	MinValue = "Which can be set with `MinValue` & `MaxValue` for can be set with a Predetermined Color Pallet",

	ColorName = "`ColorName` sets the predetermined color pallets, with the options of {'sunset', 'ocean', 'fire', 'red'}"
)

c.ModulusValue = 3 # Must be set if the Shadow Style set for the Generation is `modulus`
```

### Implimenting the Settings
 - To Make the settings set in the two previous examples apply, they must be put into the `Kyros.fractal.SetAll()` function

```python
import Kyros

f = Kyros.fractal()

f.SetAll(settings = settings, clr = c)
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

# Quickstart::
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
	"GenType": "SD TD"
}

f = Kyros.fractal()
f.SetAll(settings)
f.TurtleSetup()
```

# Notes
 - `self.color.ModulusValue` in the information file always says that it is set to `None`, this is because the data is written before that variable is set. In the future this will be changed into a configurable interface for passing the color function into the fractal object. 
# Current Work::
### See `TODO.md` to see what is being worked

---
**Documentation** *[Coming Soon]*
