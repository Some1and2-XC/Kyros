# TODO List
 - Lean in more with the generation function have more of an OOP approach (inheriting eval function as well as 3D abilities rather than the current approach which is more procedural). 
 - Make setting the color before any of the other settings something that is required instead of having the option for some of the thigns that would be printed to the information file being not used
 - Make all exports from any kind of `Animate()` function __**ONLY MAKE A `.mov` OR `.mp4` NOT `.gif`**__
 - Make the `GetData()` function reference `SetAll()`
 - Fix Topleft Broken Pixel Problem on `SD TD`
 - Changing the modulus function from `self.color.x()` to throw a custom `ModulusError` could be useful because if that is sent to the `self.eval()` function for something similair, a more useful error message could be thrown
 - Fix and remove `self.v`
 - Fix Spelling Mistakes
 - Write Data Dictionary for the inputs for the setup data that needs to be set. 

# Notes
 - `self.color.ModulusValue` in the information file always says that it is set to `None`, this is because the data is written before that variable is set. A solution to this would be to require that the color function is fully setup beforehand then passing the color function into `self.SetAll()`