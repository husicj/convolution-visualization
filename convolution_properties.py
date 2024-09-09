import numpy as np

from visualize_convolution import *

SAMPLE_WIDTH = 0.01 # adjusts the precision of the computation
X_BOUNDS = (-3, 3) # should be symmetrical because the exponential has unbounded support
TEST_RANGE = np.linspace(-3, 3, 50) # range of values over which the properties are tested

functions = ConvolutionFunctions()
conv = Convolution(SAMPLE_WIDTH, X_BOUNDS)
# Commutativity
print("Commutativity:")
for f in functions:
    for g in functions:
        fg = conv.convolve(f, g)
        gf = conv.convolve(g, f)
        acc_commutative = 0
        for t in TEST_RANGE:
            acc_commutative += (fg(t) - gf(t)) ** 2
        print(f"(f: {f.__name__}; g: {g.__name__}) " +
              f"RMSD between f * g and g * f: {np.sqrt(acc_commutative/len(TEST_RANGE))}")

# Associativity
print("\nAssociativity:")
for f in functions:
    for g in functions:
        for h in functions:
            acc_associative = 0
            f_gh = conv.convolve(f, conv.convolve(g, h))
            fg_h = conv.convolve(conv.convolve(f, g), h)
            for t in TEST_RANGE:
                acc_associative += (f_gh(t) - fg_h(t)) ** 2
            print(f"(f: {f.__name__}; g: {g.__name__}) " +
                  f"RMSD between f*(g*h) and (f*g)*h: {np.sqrt(acc_associative/len(TEST_RANGE))}")

# Distributivity
print("\nDistributivity:")
for f in functions:
    for g in functions:
        for h in functions:
            acc_distributive = 0
            f_gplush = conv.convolve(f, lambda t: g(t) + h(t))
            fg_plus_fh = lambda t: conv.convolve(f, g)(t) + conv.convolve(f, h)(t)
            for t in TEST_RANGE:
                acc_distributive += (f_gplush(t) - fg_plus_fh(t)) ** 2
            print(f"(f: {f.__name__}; g: {g.__name__}) " +
                  f"RMSD between f*(g+h) and (f*g)+(f*h): {np.sqrt(acc_associative/len(TEST_RANGE))}")

# Identity
