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

# class SamplingGrid(np.ndarray):
#     """A two-dimensional grid of points at which a function can
#        be sampled for visualization."""

#     def __init__(self, dimensions: tuple[float, float]):
#         pass

class DataVisualizer:
    """A class containing the parameters necessary for the
       visualization of the data produced in this project."""

    def __init__(self,
                 domain: tuple[float, float],
                 resolution: float
                 ):
        self.x = np.linspace(domain[0], domain[1], resolution)
        self.domainSize = domain[1] - domain[0]
        self.x_min = domain[0]
        self.x_max = domain[1]
        self.y_min = 0
        self.y_max = 10

    def show_animation(self, update_list):
        fig, axs = plt.subplots(len(update_list))
        for ax in axs:
            ax.set(xlim=[self.x_min, self.x_max])
            ax.set(ylim=[self.y_min, self.y_max])

        def update(frame: int):
            for i, update_func in enumerate(update_list):
                plot = axs[i].plot([], [])[0]
                update_func(plot, frame)

        ani = animation.FuncAnimation(fig=fig,
                                      func=update,
                                      frames=len(self.x),
                                      interval=15)
        
        plt.show()

    def function_plotter(self, function: typing.Callable[[float], float]):
        x = self.x
        y = function(x)

        def update(plot: matplotlib.lines.Line2D, frame: int):
            X = x[:frame]
            Y = y[:frame]
            plot.set_xdata(X)
            plot.set_ydata(Y)
            return plot

        return update


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
    dv = DataVisualizer((-10, 10), 100)
    f = dv.function_plotter(lambda x: x*x/10)
    dv.show_animation([f, f])
