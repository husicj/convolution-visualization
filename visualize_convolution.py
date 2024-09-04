# GOALS:
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



if __name__ == '__main__':
    dv = DataVisualizer((-10, 10), (-2, 2), 500, 500)
    t = np.linspace(-10, 10, 101)
    def rectangle(x, t):
        return (np.abs(x - t) < 0.5).astype(float)
    dv.parameter_animation(rectangle, dv.x, t)
    dv.animation.save('parameter_test')

