#GOALS:
#   generate visualizations of convolutions between:
#      rectangle
#      isoceles triangle
#      right triangle
#      causally decreasing exponential function
#
#   computationally confirm the following properties of convolution
#    with RMS error calculation:
#     commutativity
#     assiciativity
#     distributivity
#   and demonstrating through animation the multiplicative identity

import typing

# import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from PIL import ImageDraw

class Plotting_Image:
    """A data structure representing an image, along with a number of
       methods for modifying the image such as plotting points and
       adding text."""

    def __init__(self,
                 x_bounds: tuple[float, float],
                 y_bounds: tuple[float, float],
                 a_size: int = 100,
                 b_size: int = 100):
        self.image_array = np.zeros((a_size, b_size))
        self.a_size = a_size
        self.b_size = b_size
        self.x_min = x_bounds[0]
        self.x_max = x_bounds[1]
        self.x_size = self.x_max - self.x_min
        self.y_min = y_bounds[0]
        self.y_max = y_bounds[1]
        self.y_size = self.y_max - self.y_min

    def _coordinate_to_pixel(self, x: float | np.ndarray, y: float | np.ndarray) -> (int, int):
        if type(x) == 'int':
            b = int((self.b_size - 1) * (x - self.x_min) / self.x_size)
        else:
            b = ((self.b_size - 1) * (x - self.x_min) / self.x_size).astype(int)
        if type(y) == 'int':
            a = self.a_size - int((self.a_size - 1) * (y - self.y_min) / self.y_size)
        else:
            a = self.a_size - ((self.a_size - 1) * (y - self.y_min) / self.y_size).astype(int)
        return a, b


    def clear(self) -> typing.Self:
        self.image_array *= 0
        return self

    def copy(self) -> typing.Self:
        ret = Plotting_Image((self.x_min, self.x_max),
                             (self.y_min, self.y_max),
                             self.a_size,
                             self.b_size)
        ret.image_array = self.image_array.copy()
        return ret

    def plot(self, x: int | np.ndarray,
             y: int | np.ndarray,
             thickness: int = 0
             ) -> None:
        a, b = self._coordinate_to_pixel(x, y)
        if type(y) != 'int' or type(x) != 'int':
            inside_bounds = (a >= 0) * (a < self.a_size) * (b >= 0) * (b < self.b_size)
            a = a[inside_bounds]
            b = b[inside_bounds]
        try:
            self.image_array[a, b] = 255
            if thickness > 0:
                for pixel in range(thickness):
                    self.image_array[a, b + pixel] = 255
                    self.image_array[a, b - pixel] = 255
        except IndexError:
            pass

    def save(self, filename: str) -> None:
        pass

    def show(self) -> None:
        plt.imshow(self.image_array)
        plt.show()

class Animation:
    """A collection of Plotting_Image objects that represents an animation."""

    def __init__(self, image_list: typing.List[Plotting_Image]):
        self.image_list = image_list

    def save(self, filename: str) -> None:
        images = []
        for frame, image in enumerate(self.image_list):
            images.append(Image.fromarray(image.image_array))
            drawing = ImageDraw.Draw(images[-1])
            drawing.text((10,10), f"{frame}", fill=255)
        images[0].save(filename + '.gif', append_images=images[1:], save_all=True, duration=1)


class DataVisualizer:
    """A class containing the parameters necessary for the
       visualization of the data produced in this project."""

    def __init__(self,
                 x_bounds: tuple[float, float],
                 y_bounds: tuple[float, float],
                 x_resolution: float,
                 y_resolution: float
                 ):
        self.canvas = Plotting_Image(x_bounds, y_bounds, x_resolution, y_resolution)
        self.line_thickness = 2

        self.x_min = x_bounds[0]
        self.x_max = x_bounds[1]
        self.y_min = y_bounds[0]
        self.y_max = y_bounds[1]
        self.x = np.linspace(x_bounds[0], x_bounds[1], x_resolution)
        self.y = np.linspace(y_bounds[0], y_bounds[1], y_resolution)
        self.domainSize = x_bounds[1] - x_bounds[0]

    def function_plotter(self,
                         function: typing.Callable[[float], float],
                         x: np.ndarray
                         ) -> Plotting_Image:
        y = function(x)
        self.canvas.plot(x, y, self.line_thickness)
        return self.canvas.copy()

    def function_animation(self,
                           function: typing.Callable[[float], float],
                           x: np.ndarray
                           ) -> Animation:
        animation_list = []
        for frame in range(len(x)):
            animation_list.append(self.function_plotter(function, x[frame]))
        self.animation = Animation(animation_list)
        return self.animation

    def parameter_plotter(self,
                          function: typing.Callable[[float, float], float],
                          x: np.ndarray,
                          t: float
                          ) -> Plotting_Image:
        y = function(x, t)
        self.canvas.plot(x, y, self.line_thickness)
        return self.canvas.copy()

    def parameter_animation(self,
                               function: typing.Callable[[float, float], float],
                               x: np.ndarray,
                               t: np.ndarray
                            ) -> Animation:
        animation_list = []
        for frame in range(len(t)):
            self.canvas.clear()
            animation_list.append(self.parameter_plotter(function, x, t[frame]))
        self.animation = Animation(animation_list)
        return self.animation

class Convolution:
    def __init__(self, sample_width: float, xbounds: tuple[float, float]):
        self.sample_width = sample_width
        self.x_min = xbounds[0]
        self.x_max = xbounds[1]
        self.sample_count = 1 + int((self.x_max - self.x_min) / self.sample_width)
        self.sampling = np.linspace(self.x_min, self.x_max, self.sample_count)
        
    def convolve(self,
                 f: typing.Callable[[float], float], 
                 g: typing.Callable[[float], float]
                 ) -> typing.Callable[[float], float]:
        # precompute the sampling of f and the multiplication by the sample width
        # so that it does not need to be repeated for each function call
        scaled_sampled_f = self.sample_width * f(self.sampling)
        def convolution(x: float) -> float:
            return (scaled_sampled_f * g(x - self.sampling)).sum()
        return convolution

class ConvolutionFunctions:
    """A class containing all the relevant functions for convolution and plotting."""

    def rectangle(x: float, t: float = 0) -> float:
        """Rectangle function with height and width 1, centered at t."""
        return (np.abs(x - t) < 0.5).astype(float)

    def right_triangle(x: float, t: float = 0) -> float:
        """Downward sloping isoceles right triangle with height 1, and discontinuity at t."""
        return (0 <= x - t).astype(float) * (x - t < 1).astype(float) * (1 - x + t)

    def isoceles_triangle(x: float, t: float = 0) -> float:
        """Isoceles right triangle with base along x axis, with height 1, base 2, and centered at 0."""
        return (np.abs(x - t) < 1).astype(float) * (1 - np.abs(x - t))

    def exponential(x: float, t: float = 0) -> float:
        """Decreasing exponential function with y = 1 at x = t."""
        return np.exp(t - x)

if __name__ == '__main__':
    dv = DataVisualizer((-2, 2), (-2, 2), 500, 500)
    t = np.linspace(-2, 2, 100)
    # dv.parameter_animation(ConvolutionFunctions.exponential, dv.x, t)
    conv = Convolution(0.001, (-3, 3))
    fg = conv.convolve(ConvolutionFunctions.rectangle, ConvolutionFunctions.right_triangle)
    plot = dv.function_animation(fg, dv.x)
    plot.save('conv')
