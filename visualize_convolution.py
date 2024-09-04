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

import matplotlib.axes
import matplotlib.animation as animation
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


    def clear(self):
        self.image_array *= 0

    def copy(self):
        ret = Plotting_Image((self.x_min, self.x_max),
                             (self.y_min, self.y_max),
                             self.a_size,
                             self.b_size)
        ret.image_array = self.image_array.copy()
        return ret

    def plot(self, x: int | np.ndarray, y: int | np.ndarray):
        a, b = self._coordinate_to_pixel(x, y)
        if type(y) != 'int' or type(x) != 'int':
            inside_bounds = (a >= 0) * (a < self.a_size) * (b >= 0) * (b < self.b_size)
            a = a[inside_bounds]
            b = b[inside_bounds]
        try:
            self.image_array[a, b] = 255
        except IndexError:
            print(f"Cannot plot point ({x}, {y}): it lies outside of the plotting canvas.")
            print((a, b))

    def save(self, filename: str):
        pass

    def show(self):
        plt.imshow(self.image_array)
        plt.show()

class Animation:
    """A collection of Plotting_Image objects that represents an animation."""

    def __init__(self, image_list: typing.List[Plotting_Image]):
        self.image_list = image_list

    def save(self, filename: str):
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

        self.x_min = x_bounds[0]
        self.x_max = x_bounds[1]
        self.y_min = y_bounds[0]
        self.y_max = y_bounds[1]
        self.x = np.linspace(x_bounds[0], x_bounds[1], x_resolution)
        self.y = np.linspace(y_bounds[0], y_bounds[1], y_resolution)
        self.domainSize = x_bounds[1] - x_bounds[0]

    def function_plotter(self, function: typing.Callable[[float], float], x: np.ndarray):
        y = function(x)
        self.canvas.plot(x, y)
        return self.canvas.copy()

    def plot_animation(self, function: typing.Callable[[float], float], x: np.ndarray):
        animation_list = []
        for frame in range(len(x)):
            animation_list.append(self.function_plotter(function, x[frame]))
        print(len(animation_list))
        self.animation = Animation(animation_list)
        return self.animation

    def parameter_plotter(self,
                          function: typing.Callable[[float, float], float]):
        t = 0
        x = self.x
        y = function(x, t)
        self.y_min = 1.1 * min(self.y_min, np.min(y))
        self.y_max = 1.1 * max(self.y_max, np.max(y))
        fig, ax = plt.subplots()
        func_plot = ax.plot(x, y)[0]
        ax.set(xlim=[self.x_min, self.x_max],
               ylim=[self.y_min, self.y_max])

        def update(frame: int):
            X = x
            Y = function(x, frame)
            func_plot.set_xdata(X)
            func_plot.set_ydata(Y)
            return func_plot

        ani = animation.FuncAnimation(fig=fig,
                                      func=update,
                                      frames=150,
                                      interval=100)

        plt.show()



if __name__ == '__main__':
    dv = DataVisualizer((0, 10), (0, 100), 500, 500)
    dv.plot_animation(lambda x: x*x, dv.x)
    dv.animation.save('test')

