# TODO list
 - Add the ability to set unique color pallets, more than the preset ones
 - Remove half of the code describing math because more of it is copy & pasted
 - Add the ability to render frames without turtle, having the `self.TurtleSetup()` function just run the `self.render()` function then set the created image as the background
 - Make the `ThreeDeeify` module that is not being used into an attribute of Kyros.fractal()
 - Make `ThreeDeeify` work
    - The problem with ThreeDeeify is that it is impossible to send the coloring funtion to it without having the coloring function not be based on immdiate values
    - Having the color function be set as a variable to be passed to `ThreeDeeify` would be a solution
 - Change the viewing window from turtle to something closer to tkinter (as turtle is a wrapper for tkinter)

---
