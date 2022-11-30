# TODO List
 - Make setting the color before any of the other settings something that is required instead of having the option for some of the thigns that would be printed to the information file being not used
 - Make all exports from any kind of `Animate()` function __**ONLY MAKE A `.mov` OR `.mp4` NOT `.gif`**__
 - Fix Topleft Broken Pixel Problem on `SD TD`
 - Changing the modulus function from `self.color.x()` to throw a custom `ModulusError` could be useful because if that is sent to the `self.eval()` function for something similair, a more useful error message could be thrown
 - See if having a `SetFunction()` attribute of the `fractal()` class is nessessary. 
 - Make `FixArrayDimensions()` function in `fractal.eval()` be used
 - Add functionality to make the color function convert values to different number formats (dec, hex, bin, oct etc) and convery back to dec incorrectly (3 (in decimal) -> 11 (in binary) -> 11 (in decimal))
# Notes
 - `self.color.ModulusValue` in the information file always says that it is set to `None`, this is because the data is written before that variable is set. A solution to this would be to require that the color function is fully setup beforehand then passing the color function into `self.SetAll()`