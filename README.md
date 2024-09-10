#Visualizing Convolutions
##Joren Husic

## Running the code
This code has been tested with Python 3.11. It uses a number of features
from recent versions of Python, particularly in regards to type
annotations, and may not run properly on older versions.

Modules required for running the two programs included here can be found
in requirements.txt. To generate the animations demonstrating how
convolution works intuitively, run
```
python visualize_convolution.py
```
This will result in the creating of 6 .gif files containing the
animations, labeled according to the pair of functions in that
animation.

To run the script that evaluates the validity of a number of properties
of convolutions for the various example functions, run
```
python convolution_properties.py
```
This will display the RMSD values that are expected to be nearly zero
for the properties being tested, checked for the various pairwise
combinations of functions also used for the visualizations. Additionally,
this script produces four additional .gif files, demonstrating that
convolution with (an approximation of) a delta function acts as the
identity. Finally, a summary of the RMSD calculations will be printed to
the terminal, listing the average RMSD across the different pairwise
tests of the properties.
