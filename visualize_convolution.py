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

import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from PIL import ImageDraw

class PlottingImage:
    """A data structure representing an image, along with a number of
       methods for modifying the image such as plotting points and
       adding text."""

    def __init__(self,
                 x_bounds: tuple[float, float],
                 y_bounds: tuple[float, float],
                 a_size: int = 100,
                 b_size: int = 100,
                 show_axes: bool = True,
                 base_image_array: None | np.ndarray = None):
        self.image_array = np.zeros((a_size, b_size, 3))
        self.update_base_image(base_image_array)
        self.a_size = a_size
        self.b_size = b_size
        self.x_min = x_bounds[0]
        self.x_max = x_bounds[1]
        self.x_size = self.x_max - self.x_min
        self.y_min = y_bounds[0]
        self.y_max = y_bounds[1]
        self.y_size = self.y_max - self.y_min
        self.show_axes = show_axes
        if self.show_axes:
            self.draw_axes()

    def _coordinate_to_pixel(self, x: float | np.ndarray, y: float | np.ndarray) -> (int, int):
        """Converts Cartesian coordinates to pixel coordinates so that a point
        can be drawn onto an the image."""
        if type(x) == float:
            b = int((self.b_size - 1) * (x - self.x_min) / self.x_size)
        else:
            b = ((self.b_size - 1) * (x - self.x_min) / self.x_size).astype(int)
        if type(y) == float:
            a = self.a_size - int((self.a_size - 1) * (y - self.y_min) / self.y_size)
        else:
            a = self.a_size - ((self.a_size - 1) * (y - self.y_min) / self.y_size).astype(int)
        return a, b

    def clear(self) -> typing.Self:
        """Resets the image to self.base_image_array."""
        self.image_array = self.base_image_array.copy()
        return self

    def copy(self) -> typing.Self:
        """Returns a copy of this object that can be passed by by reference safely."""
        ret = PlottingImage((self.x_min, self.x_max),
                             (self.y_min, self.y_max),
                             self.a_size,
                             self.b_size,
                             base_image_array=self.base_image_array)
        ret.image_array = self.image_array.copy()
        return ret

    def draw_axes(self):
        """Draw coordinate axes of the Cartesian plane onto the image."""
        y_axis, x_axis = self._coordinate_to_pixel(0., 0.)
        y_integer_bounds = (np.floor(self.y_min + 1).astype(int), np.ceil(self.y_max - 1).astype(int))
        x_integer_bounds = (np.floor(self.x_min + 1).astype(int), np.ceil(self.x_max - 1).astype(int))
        # drawing the grid
        for y in np.linspace(y_integer_bounds[0], -1, np.abs(y_integer_bounds[0])):
            a, b = self._coordinate_to_pixel(0., y)
            self.image_array[a, :] = np.asarray([64, 64, 64])
        for x in np.linspace(x_integer_bounds[0], -1, np.abs(x_integer_bounds[0])):
            a, b = self._coordinate_to_pixel(x, 0.)
            self.image_array[:, b] = np.asarray([64, 64, 64])
        for y in np.linspace(1, y_integer_bounds[1], np.abs(y_integer_bounds[1])):
            a, b = self._coordinate_to_pixel(0., y)
            self.image_array[a, :] = np.asarray([64, 64, 64])
        for x in np.linspace(1, x_integer_bounds[1], np.abs(x_integer_bounds[1])):
            a, b = self._coordinate_to_pixel(x, 0.)
            self.image_array[:, b] = np.asarray([64, 64, 64])
        # drawing the axes
        self.image_array[y_axis, :] = np.asarray([128, 128, 128])
        self.image_array[:, x_axis] = np.asarray([128, 128, 128])


    def plot(self, x: int | np.ndarray,
             y: int | np.ndarray,
             thickness: int = 0,
             color: tuple[int, int, int] = (255, 255, 255)
             ) -> None:
        """Draw a point in Cartesian space onto the image."""
        a, b = self._coordinate_to_pixel(x, y)
        if type(y) != 'int' or type(x) != 'int':
            inside_bounds = (a >= 0) * (a < self.a_size) * (b >= 0) * (b < self.b_size)
            a = a[inside_bounds]
            b = b[inside_bounds]
        try:
            self.image_array[a, b] = np.asarray(color)
            if thickness > 0:
                for pixel in range(thickness):
                    self.image_array[a, b + pixel] = np.asarray(color)
                    self.image_array[a, b - pixel] = np.asarray(color)
        except IndexError:
            pass

    def show(self) -> None:
        """Shows the image using matplotlib for quick reference."""
        plt.imshow(self.image_array)
        plt.show()

    def update_base_image(self, image_array: None | np.ndarray = None):
        """Sets the current image array as the base image array,
        which is the image that the image array is reset to whenever
        clear() is called."""
        if image_array is None:
            self.base_image_array = self.image_array.copy()
        else:
            self.base_image_array = image_array

class Animation:
    """A collection of PlottingImage objects that represents an animation."""

    def __init__(self, image_list: typing.List[PlottingImage]):
        self.image_list = image_list
        self.title = ""
        self.legend = []

    def copy(self) -> typing.Self:
        """Returns a copy of this object that can be passed by reference safely."""
        return Animation(self.image_list.copy())

    def _draw_legend(self, drawing):
        """Draw the plot legend onto the images in the animation."""
        for i, item in enumerate(self.legend):
            drawing.text((400, 60 + 10 * i), item[0], fill=item[1])

    def save(self, filename: str) -> None:
        """Save the animation to a .gif file."""
        images = []
        for frame, image in enumerate(self.image_list):
            # reordering dimensions to format taken by PIL.Image
            image_array = image.image_array.astype('uint8')
            images.append(Image.fromarray(image_array, mode='RGB'))
            drawing = ImageDraw.Draw(images[-1])
            drawing.text((10,10), f"{frame}", fill=(255, 255, 255))
            drawing.text((30, 30), self.title, fill=(255, 255, 255))
            self._draw_legend(drawing)
        images[0].save(filename + '.gif', append_images=images[1:], save_all=True, duration=1)

    def add_title(self, title: str):
        """Add a title to the images in the animation."""
        self.title = title

    def add_legend(self, legend: list):
        """Add a legend to the images in the animation."""
        self.legend = legend


class DataVisualizer:
    """A class containing the parameters necessary for the
       visualization of the data produced in this project."""

    def __init__(self,
                 x_bounds: tuple[float, float],
                 y_bounds: tuple[float, float],
                 x_resolution: float,
                 y_resolution: float
                 ):
        self.canvas = PlottingImage(x_bounds, y_bounds, x_resolution, y_resolution)
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
                         x: np.ndarray,
                         color: tuple[int, int, int] = (255, 255, 255)
                         ) -> PlottingImage:
        """Plots a function at the values in x onto the canvas."""
        y = function(x)
        self.canvas.plot(x, y, self.line_thickness, color=color)
        return self.canvas.copy()

    def function_animation(self,
                           function: typing.Callable[[float], float],
                           x: np.ndarray,
                           frame_spacing: int = 1,
                           color: tuple[int, int, int] = (255, 255, 255)
                           ) -> Animation:
        """Creates an animation plotting a function from the lower x bound
        of the canvas to the upper x bound."""
        animation_list = []
        for frame in range(len(x)):
            plot = self.function_plotter(function, x[frame], color=color)
            # add every (frame_spacing)-th image to animation
            if not (frame % frame_spacing):
                animation_list.append(plot)
        self.animation = Animation(animation_list)
        return self.animation.copy()

    def lock_canvas(self) -> PlottingImage:
        """Saves the current canvas as the default state of the canvas.
        When canvas.clear() is called, it will return the canvas to this
        state."""
        self.canvas.update_base_image()
        return self.canvas.copy()

    def parameter_plotter(self,
                          function: typing.Callable[[float, float], float],
                          x: np.ndarray,
                          t: float,
                          color: tuple[int, int, int] = (255, 255, 255)
                          ) -> PlottingImage:
        """Plots a function on the range of x values, for a given parameter
        of the function t."""
        y = function(x, t)
        self.canvas.plot(x, y, self.line_thickness, color=color)
        return self.canvas.copy()

    def parameter_animation(self,
                            function: typing.Callable[[float, float], float],
                            x: np.ndarray,
                            t: np.ndarray,
                            frame_spacing: int = 1,
                            color: tuple[int, int, int] = (255, 255, 255)
                            ) -> Animation:
        """Plots an animation of a family of functions of x onto the canvas,
        varying the parameter t of the family for each frame."""
        animation_list = []
        for frame in range(len(t)):
            # add every (frame_spacing)-th image to animation
            if not (frame % frame_spacing):
                self.canvas.clear()
                plot = self.parameter_plotter(function, x, t[frame], color=color)
                animation_list.append(plot)
        self.animation = Animation(animation_list)
        return self.animation.copy()

    def function_and_parameter_animation(self,
                                         function: typing.Callable[[float], float],
                                         parameter_function: typing.Callable[[float, float], float],
                                         x: np.ndarray,
                                         t: np.ndarray,
                                         frame_spacing: int = 1,
                                         function_color: tuple[int, int, int] = (255, 255, 255),
                                         parameter_function_color: tuple[int, int, int] = (255, 255, 255)
                                         ) -> Animation:
        """Performs the function and parameter plotter animations
        simultaneously to the canvas."""
        animation_list = []
        for frame in range(len(t)):
            # add every (frame_spacing)-th image to animation
            function_plot = self.function_plotter(function, x[frame], color=function_color)
            self.lock_canvas()
            if not (frame % frame_spacing):
                parameter_plot = self.parameter_plotter(parameter_function, x, t[frame], color=parameter_function_color)
                animation_list.append(parameter_plot)
                self.canvas.clear()
        self.animation = Animation(animation_list)
        return self.animation.copy()

    def visualize_convolution(self,
                              f: typing.Callable[[float, float], float],
                              g: typing.Callable[[float, float], float],
                              frame_spacing: int = 1
                              ) -> Animation:
        """Creates an animation to visualize the convolution of the
        functions f and g."""
        self.function_plotter(f, self.x, color = (255, 0, 0))
        self.lock_canvas()
        # a convolution sampling two x values for every pixel
        convolution = Convolution((self.x[1] - self.x[0])/2, (self.x_min, self.x_max))
        f_conv_g = convolution.convolve(f, g)
        # g is reversed in plotting to match the definition of convolution
        return self.function_and_parameter_animation(f_conv_g,
                                                     lambda x, t: g(-x, -t),
                                                     self.x,
                                                     self.x,
                                                     frame_spacing=5,
                                                     function_color=(0,255,0),
                                                     parameter_function_color=(0,0,255)
                                                     )

class Convolution:
    """Contains the parameters for calculating the convolution of two functions.
    Shrinking the sample_width will lead to more precise computation of the convolution,
    but greatly increases computation time."""
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
        """Returns a function that is the finitely sampled convolution of the functions
        f and g that it is passed. The precision of this sampling is determined by
        the containing instance."""
        # precompute the sampling of f and the multiplication by the sample width
        # so that it does not need to be repeated for each function call
        scaled_sampled_f = self.sample_width * f(self.sampling)
        def convolution(x: float | np.ndarray) -> float | np.ndarray:
            if type(x) == np.ndarray:
                out = []
                for x_value in x:
                    out.append((scaled_sampled_f * g(x_value - self.sampling)).sum())
                return np.asarray(out)
            else:
                return (scaled_sampled_f * g(x - self.sampling)).sum()
        return convolution

class ConvolutionFunctions:
    """A class containing all the relevant functions for convolution and plotting."""

    def rectangle(x: float, t: float = 0) -> float:
        """Rectangle function with height and width 1, centered at t."""
        return (np.abs(x - t) < 0.5).astype(float)

    def right_triangle(x: float, t: float = 0) -> float:
        """Downward sloping isoceles right triangle with height 1, and centered at t."""
        return (np.abs(x - t) < 0.5).astype(float) * (0.5 - x + t)

    def isoceles_triangle(x: float, t: float = 0) -> float:
        """Isoceles right triangle with base along x axis, with height 1, base 2, and centered at 0."""
        return (np.abs(x - t) < 1).astype(float) * (1 - np.abs(x - t))

    def exponential(x: float, t: float = 0) -> float:
        """Causally decreasing exponential function with y = 1 at x = t."""
        return (0 <= x - t).astype(float) * np.exp(t - x)

if __name__ == '__main__':
    dv0 = DataVisualizer((-2, 2), (-2, 2), 500, 500)
    plot0 = dv0.visualize_convolution(ConvolutionFunctions.rectangle,
                                      ConvolutionFunctions.right_triangle,
                                      frame_spacing=5)
    plot0.add_title("Convolution of rectangle and right triangle functions")
    plot0.add_legend([("rectangle", (255,0,0)), ("right triangle", (0,0,255)), ("convolution", (0,255,0))])
    plot0.save('rectangle_and_right_triangle')

    dv1 = DataVisualizer((-2, 2), (-2, 2), 500, 500)
    plot1 = dv1.visualize_convolution(ConvolutionFunctions.rectangle,
                                      ConvolutionFunctions.isoceles_triangle,
                                      frame_spacing=5)
    plot1.add_title("Convolution of rectangle and isoceles triangle functions")
    plot1.add_legend([("rectangle", (255,0,0)), ("isoceles triangle", (0,0,255)), ("convolution", (0,255,0))])
    plot1.save('rectangle_and_isoceles_triangle')

    dv2 = DataVisualizer((-1.5, 2.5), (-2, 2), 500, 1000)
    plot2 = dv2.visualize_convolution(ConvolutionFunctions.rectangle,
                                      ConvolutionFunctions.exponential,
                                      frame_spacing=5)
    plot2.add_title("Convolution of rectangle and truncated exponential functions")
    plot2.add_legend([("rectangle", (255,0,0)), ("exponential", (0,0,255)), ("convolution", (0,255,0))])
    plot2.save('rectangle_and_exponential')

    dv3 = DataVisualizer((-2, 2), (-2, 2), 500, 500)
    plot3 = dv3.visualize_convolution(ConvolutionFunctions.right_triangle,
                                      ConvolutionFunctions.isoceles_triangle,
                                      frame_spacing=5)
    plot3.add_title("Convolution of right triangle and isoceles triangle functions")
    plot3.add_legend([("right triangle", (255,0,0)), ("isoceles triangle", (0,0,255)), ("convolution", (0,255,0))])
    plot3.save('right_and_isoceles_triangles')

    dv4 = DataVisualizer((-1.5, 2.5), (-2, 2), 500, 500)
    plot4 = dv4.visualize_convolution(ConvolutionFunctions.right_triangle,
                                      ConvolutionFunctions.exponential,
                                      frame_spacing=5)
    plot4.add_title("Convolution of right triangle and truncated exponential functions")
    plot4.add_legend([("exponential", (0,0,255)), ("right triangle", (255,0,0)), ("convolution", (0,255,0))])
    plot4.save('right_triangle_and_exponential')

    dv5 = DataVisualizer((-1.5, 2.5), (-2, 2), 500, 500)
    plot5 = dv5.visualize_convolution(ConvolutionFunctions.isoceles_triangle,
                                      ConvolutionFunctions.exponential,
                                      frame_spacing=5)
    plot5.add_title("Convolution of isoceles triangle and truncated exponential functions")
    plot5.add_legend([("isoceles triangle", (255,0,0)), ("exponential", (0, 0, 255)), ("convolution", (0,255,0))])
    plot5.save('isoceles_triangle_and_exponential')
