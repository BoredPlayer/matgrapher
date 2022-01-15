# matgrapher
An easy to use python class aiding with matplotlib graph making. It provides a set of methods automating typical usecases of matplotlib graph drawing.

## Dependencies
In order to work properly, the program needs 2 external libraries:

1) matplotlib (avaliable at [matplotlib.org](https://matplotlib.org/stable/users/getting_started/index.html#installation-quick-start) site)
2) numpy (avaliable at [numpy.org](https://numpy.org/install/) site)

Both should be installed automatically while using pip.

## Installation
To install the library just type in terminal:
```
pip install git+https://github.com/BoredPlayer/matgrapher.git
```

## Usage
List of all commands in recommended order (a TL;DR if You wish) is presented at the bottom of this chapter.

Importing the library may be done using:
```
from matgrapher import grapher
```

In order to initialise the grapher object, assign it to a variable:
```
gr = grapher() # gr is just an example variable name, feel free to call it differently
```

It is recomended, that data labels are loaded before the data itself, however it is not necessary. In order to load data to grapher's internal arrays, use `loadLabels()` method. As arguments it accepts at least one string, containing labels of data sets used in legend generation. If no labels are provided, legend will not be shown. If more sets of data are loaded than overall provided labels, a warning will be rised, however it does not affect the flow of the program. Example of usage is shown below:
```
gr.loadLabels(label1, label2, "last dataset") # label1 and label2 are strings to be shown in chart's legend
```

For easier data visualisation, it can be stored in grapher's local arrays using `loadData()` method. As arguments the method accepts at least 2 one dimensional arrays consisting of x- and y-axis data. If needed, the function can load multiple sets of data, however it is important to provide it in pairs of x and y arrays. Example of use is shown below:
```
gr.loadData(x_data[0], y_data[0], x_data[1], y_data[1], x_data[2], y_data[2]) # x_data and y_data are 2-dimensional arrays containing data to be drawn
```

Generating the graph may be performed using `generateGraph()` method. Providing that all prior steps were performed, it does not require any additional arguments. However it will generate a graph titled *Graph*, x and y labels will be set as *X Values* and *Y Values* and will be saved in *output* folder as *file.png*. In order to change the listed parameters, user can provide arguments such as:
1) data_x ([float, ...]) - data shown as argument X of the drawn chart,
2) data_y ([float, ...]) - data shown as argument Y of the drawn chart,
3) axis_names ([string, string]) - table of axis names ([0] - X axis, [1] - Y axis]),
4) graph_title (string) - a title for drawn graph,
5) legend ([string, ...]) - tabe of labels used in legend,
6) filename (string) - name for the output file,
7) dpi (int) - Dots Per Inch (resolution) of the exported graph,
8) plot_size ([float, float]) - size of the exported graph (in inches - conversion ratio cm->inch is 1/2.54),
9) grid (boolean) - argument for generating grid in the drawn graph
10) save (boolean) - flag for saving drawn graph
11) show (boolean) - flag for showing drawn graph

After drawing the plot, figure created will be closed as per matplotlib documentation's recomendation.

Example of use:
```
gr.generateGraph(axis_names=[r"time $\left [ s \right ]$", r"$C_D, C_L$"], graph_title=r"Simulated $C_L$ and $C_D$ values in time", filename="output/CLCDtime.png", grid=True)
```

If it is necessary to draw a new set of data, the data currently loaded can be removed by using the `destroyGraphTable()`. The method requires no arguments and will clear all of loaded data.

All of commands in recommended order:
```
from grapher import grapher
gr=grapher()
gr.loadLabels(label1, label2)
gr.loadData(x_data1, y_data1, x_data2, y_data2)
gr.generateGraph()
gr.destroyGraphTable()
```
