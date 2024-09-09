import numpy as np

from visualize_convolution import *

SAMPLE_WIDTH = 0.01 # adjusts the precision of the computation
X_BOUNDS = (-3, 3) # should be symmetrical because the exponential has unbounded support
TEST_RANGE = np.linspace(-3, 3, 50) # range of values over which the properties are tested

functions = ConvolutionFunctions()
conv = Convolution(SAMPLE_WIDTH, X_BOUNDS)
# Commutativity
print("Commutativity:")
mean_commutative = 0
for f in functions:
    for g in functions:
        fg = conv.convolve(f, g)
        gf = conv.convolve(g, f)
        acc_commutative = 0
        for t in TEST_RANGE:
            acc_commutative += (fg(t) - gf(t)) ** 2
        print(f"(f: {f.__name__}; g: {g.__name__}) " +
              f"RMSD between f * g and g * f: {np.sqrt(acc_commutative/len(TEST_RANGE))}")
        mean_commutative += acc_commutative / len(TEST_RANGE) / len(functions)**2

# Associativity
print("\nAssociativity:")
mean_associative = 0
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
            mean_associative += acc_associative / len(TEST_RANGE) / len(functions)**3

# Distributivity

print("\nDistributivity:")
mean_distributive = 0
for f in functions:
    for g in functions:
        for h in functions:
            acc_distributive = 0
            f_gplush = conv.convolve(f, lambda t: g(t) + h(t))
            fg_plus_fh = lambda t: conv.convolve(f, g)(t) + conv.convolve(f, h)(t)
            for t in TEST_RANGE:
                acc_distributive += (f_gplush(t) - fg_plus_fh(t)) ** 2
            print(f"(f: {f.__name__}; g: {g.__name__}) " +
                  f"RMSD between f*(g+h) and (f*g)+(f*h): {np.sqrt(acc_distributive/len(TEST_RANGE))}")
            mean_distributive += acc_associative / len(TEST_RANGE) / len(functions)**3

# Identity
print("\nIdentity:")
for f in functions:
    dv = DataVisualizer((-2,2), (-2,2), 500, 500)
    convolution_sample_width = (dv.x[1] - dv.x[0]) / 2 # this is the same as used internally in the visualization function
    g = ConvolutionFunctions.delta
    plot = dv.visualize_convolution(f, g, frame_spacing = 5, g_is_delta = True)
    plot.add_title(f"Convolution of {f.__name__} with Dirac delta function")
    plot.add_legend([(f.__name__, (255,0,0)), ("delta", (0, 0, 255)), ("convolution", (0,255,0))])
    filename = f.__name__ + "_and_delta"
    plot.save(filename)
    print(f"Visualization of the existence of the identity for {f.__name__} found in file {filename}.gif.")

# Summary
print("\n\n")
print(f"Mean RMSD across all set of functions (commutativity):  {mean_commutative}")
print(f"Mean RMSD across all set of functions (associativity):  {mean_associative}")
print(f"Mean RMSD across all set of functions (distributivity): {mean_distributive}")
