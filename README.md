# Some1and2's Kyros - A Fractal Generator
#### Basic Class Oriented Fractal Generator with Binary Acceleration - Single Threaded, made with python
# Key Features:: 
 - Uses CPU Optimisation for faster Execution Time
 - Functionality for Various kinds of Fractals such as the `Mandelbrot`, `Julia` & `Burning Ship` fractals (and more)
 - Various Color Pallets for the Generators
 - Output File for Generator Data, Saves the Settings used to an Output file so that the settings can be Reused and Images can be Recreated at Higher Resolution etc

# Basic Usage::
```python
import Kyros

f = Kyros.fractal()

 # Function for Setting all the data at once to Preset Settings
f.SetAll()

 # Function for Getting Data through Text Box Input
f.GetData()

 # Function for setting the function used by Kyros [Very Optional]
f.SetFunction(func=function)

 # Function that opens a Turtle Window as a Display
f.TurtleSetup()

```

# Installation::
#### Windows:
```bat
pip install update
pip install wheel
python setup.py bdist_wheel
pip install \dist\<filename>
```

#### From PIP:
```bat
pip install -i https://test.pypi.org/simple/ Kyros
```
---
**Documentation** *[Soming Soon]*