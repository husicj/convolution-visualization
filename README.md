# Visualizing Convolutions

## About
This repository serves as a method for generating visualizations to
demonstrate the way that the convolution of two functions is related
to the starting functions. The convolution, defined as
$$ f \star g(\tau) = \int_{-\infty}^\infty f(t) g(\tau - t) dt$$
can be though of as related to the area of overlap between the two
functions (one of which is mirrored across the $y$ axis), with the
value of $\tau$ determining the offset of the two functions along the
$x$ axis.

There are a number of properties of the convolution that can be proven
from its definition. Computational verification of these properties
can be useful as a way to verify that the algorithm for performing the
convolution is performing as expected. Therefore, there is a second
script in this repository that serves to perform this verification,
by calculating the RMSD between two sides of what should be an equation
for a number of example convolutions sampled at a range of values,
and showing the result to be nearly zero. Additionally, the Dirac
delta function acts as the identity under convolution with other
integrable functions:
$$ f \star \delta(\tau) = \delta \star f(\tau) = f(\tau)$$
This is demonstrated with an additional animation.

## Running the code
This code has been tested with Python 3.11. It uses a number of features
from recent versions of Python, particularly in regards to type
annotations, and may not run properly on older versions.

The repository can be cloned by running
```
git clone https://github.com/husicj/convolution-visualization.git
```

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

## Notes
This documentation uses $\star$ to refer to convolution.

The delta function is approximated by a narrow Gaussian in all cases.
This is done because the nature of sampling of functions for discrete
computations of the convolution does not work well with a true delta
function. The delta function can be conceived of as the limit of a
sequence of normalized Gaussians with decreasing widths, so this
approximation works well for the cases it is used in here.
