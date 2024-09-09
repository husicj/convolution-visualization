import numpy as np

from visualize_convolution import *

SAMPLE_WIDTH = 0.001 # adjusts the precision of the computation
X_BOUNDS = (-3, 3) # should be symmetrical because the exponential has unbounded support
TEST_RANGE = np.linspace(-3, 3, 50) # range of values over which the properties are tested

functions = ConvolutionFunctions()
conv = Convolution(SAMPLE_WIDTH, X_BOUNDS)
# Commutativity
acc_commutative = 0
for f in functions:
    for g in functions:
        print(f"(f: {f.__name__}; g: {g.__name__})")
        fg = conv.convolve(f, g)
        gf = conv.convolve(g, f)
        for t in TEST_RANGE:
            acc_commutative += (fg(t) - gf(t)) ** 2
        print(f"RMSD between f * g and g * f: {np.sqrt(acc_commutative/len(TEST_RANGE))}\n")
