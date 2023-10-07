# matgrapher
An easy to use python class aiding with matplotlib graph making. It provides a set of methods automating typical usecases of matplotlib graph drawing.

Since version 0.1.3, `__main__.py` provides a UDP server functionality for graph generation. With this approach it is possible to draw matplotlib graphs with C++ software (more in chapter [Communication](#communication)). The `libraries` folder contains a C++ library as an example of implementation in language other than python.

### Table of contents:
1) [Dependencies](#dependencies)
2) [Installation](#installation)
3) [Usage](#usage)
4) [Communication](#communication)

## Dependencies
In order to work properly, the program needs 2 external libraries:

1) matplotlib (avaliable at [matplotlib.org](https://matplotlib.org/stable/users/getting_started/index.html#installation-quick-start) site)
2) numpy (avaliable at [numpy.org](https://numpy.org/install/) site)

Both should be installed automatically while using pip.

## Installation
This library may be easly installed using `pip`.

### Windows
To install the library just type in command window:
```bash
pip install git+https://github.com/BoredPlayer/matgrapher.git
```

### Linux
To install the library just type in terminal:
```bash
pip3 install git+https://github.com/BoredPlayer/matgrapher.git
```

## Usage
List of all commands in recommended order (a TL;DR if You wish) is presented at the bottom of this chapter.

### Basic use
Importing the library may be done using:
```python
from matgrapher import grapher
```

In order to initialise the grapher object, assign it to a variable:
```python
gr = grapher.grapher() # gr is just an example variable name, feel free to call it differently
```

It is recomended, that data labels are loaded before the data itself, however it is not necessary. In order to load data to grapher's internal arrays, use `loadLabels()` method. As arguments it accepts at least one string, containing labels of data sets used in legend generation. If no labels are provided, legend will not be shown. If more sets of data are loaded than overall provided labels, a warning will be rised, however it does not affect the flow of the program. Example of usage is shown below:
```python
gr.loadLabels(label1, label2, "last dataset") # label1 and label2 are strings to be shown in chart's legend
```

For easier data visualisation, it can be stored in grapher's local arrays using `loadData()` method. As arguments the method accepts at least 2 one dimensional arrays consisting of x- and y-axis data. If needed, the function can load multiple sets of data, however it is important to provide it in pairs of x and y arrays. Example of use is shown below:
```python
gr.loadData(x_data[0], y_data[0], x_data[1], y_data[1], x_data[2], y_data[2]) # x_data and y_data are 2-dimensional arrays containing data to be drawn
```

The `grapher.loadData()` method automatically assigns line widths. In order to change it, use:
```python
gr.changeLineWidth(width, index=dataindex)
```
The default value for dataindex is `None`. If it is unchanged, the method will only edit line width of the newest data set.

In order to change the default width of lines, use:
```python
gr.changeDefaultWidth(width)
```

Generating the graph may be performed using `generateGraph()` method. Providing that all prior steps were performed, it does not require any additional arguments. However it will generate a graph titled *Graph*, x and y labels will be set as *X Values* and *Y Values* and will be saved in *output* folder as *file.png*. In order to change the listed parameters, user can provide arguments such as:
1) data_x ([float, ...]) - data shown as argument X of the drawn chart,
2) data_y ([float, ...]) - data shown as argument Y of the drawn chart,
3) axis_names ([string, string]) - table of axis names ([0] - X axis, [1] - Y axis]),
4) x_lim ([float, float]) - limits of x_axis (if an empty array is passed (default), no limits are imposed)
5) y_lim ([float, float]) - limits of y_axis (if an empty array is passed (default), no limits are imposed)
6) graph_title (string) - a title for drawn graph,
7) line_styles ([string, ...]) - line styles as matplotlib argument
8) line_widths ([float, ...]) - widths of the drawn lines
9) colors ([string, ...]) - line colors as matplotlib argument
10) legend ([string, ...]) - tabe of labels used in legend,
11) legend_args (string) - arguments for plt.legend function
12) legend_position (string) - argument for legend location as matplotlib argument
13) filename (string) - name for the output file,
14) dpi (int) - Dots Per Inch (resolution) of the exported graph,
15) plot_size ([float, float]) - size of the exported graph (in inches - conversion ratio cm->inch is 1/2.54),
16) grid (boolean) - argument for generating grid in the drawn graph
17) save (boolean) - flag for saving drawn graph
18) show (boolean) - flag for showing drawn graph
19) tight_layout (boolean) - flag for enabling/disabling tight layout of the graph (default: True)
20) log_scale (string) - settings for log scale at chosen axis

After drawing the plot, figure created will be closed as per matplotlib documentation's recomendation.

Example of use:
```python
gr.generateGraph(axis_names=[r"time $\left [ s \right ]$", r"$C_D, C_L$"], graph_title=r"Simulated $C_L$ and $C_D$ values in time", filename="output/CLCDtime.png", grid=True)
```

### Clearing internal arrays
If it is necessary to draw a new set of data, the data currently loaded can be removed by using the `destroyGraphTable()`. The method requires no arguments and will clear all of loaded data.

All of commands in recommended order:
```python
from grapher import grapher
gr = grapher.grapher()
gr.loadLabels(label1, label2)
gr.loadData(x_data1, y_data1, x_data2, y_data2)
gr.generateGraph()
gr.destroyGraphTable()
```

# Communication
[Example of drawing graph with C++ is in the end of this section.](#example-of-c-implementation)

A big part of matgrapher library is an implementation of an interface for software not written in python. The `__main__.py` module acts as a server capable of receiving and processing data incoming via UDP packets. A socket used by the module listens for incoming messages in port 50553. The module is available for both Windows and Linux.

To easily run the server, use command (Windows):
```bash
python -m matgrapher
```

If you use Linux, use `python3 -m matgrapher` command instead.

After a few seconds the server will print welcome message:
```
Waiting for connection @ 127.0.0.1:50553
```
This means, that the server listens locally for connection at port 50553.

## Server commands
The server recognises the following set of commands:

There are four types of messages accepted by server:
1) server setup - controls server's overall behaviour to messages
2) graph setup - controls graph outlook, like size and axes
3) dataflow setup - begins or ends listening for data
4) data messages

Usable commands are listed below.

### Server setup
* `echo on` - turns debugging info in server console on
* `echo off` - turns debugging info in server console off
* `destroy graph` - invokes grapher.destroyGraph() method
* `end listening` - shuts the server down

### Graph setup
* `set title` - makes server wait for graph title
* `set axisnames` - makes server wait for axis labels
* `set xlims` - makes server wait for x axis range (example: '0.5,1.0')
* `set ylims` - makes server wait for y axis range (example: '0.5,1.0')
* `set exportmethod` - makes server wait for export method (save, don't show; show, don't save; save and show)
* `set filename` - makes server wait for output file name
* `set plotsize` - makes server wait for size of the plot
* `set DPI` - makes server wait for Dots Per Inch setting
* `set gridvisibility` - makes server wait for grid visibility flag status
* `set logscalemethod` - makes server wait for axis log scale method

### Dataflow setup
* `load data` - puts server into _single-column data receiving mode_
* `end load data` - ends _single-column data receiving mode_
* `load dataargs` - puts server into _double-column data receiving mode_
* `end load dataargs` - ends _double-column data receiving mode_
* `load muldata` - puts server into _multiple-column data receiving mode_
* `end load muldata` - edns _multiple-column data receiving mode_
* `load labels` - puts server into _labels receiving mode_
* `end loadlabels` - ends _labels receiving mode_

### Data messages
There are several types of data message format. All are explained in [Server modes section](#server-modes).

## Server modes
Typically, the server operates by waiting for a command, after which it waits for a argument associated with said command. However, there are situations requireing providing more than one line of arguments. For such situations the server can be put into one of four modes at a time:
1. _single-column data receiving mode_
2. _double-column data receiving mode_
3. _multiple-column data receiving mode_
4. _labels receiving mode_

### _single-column data receiving mode_
This mode enables sending one column of data at a time. Due to a low capacity of such transfer it is the slowest data-sending mode. The expected structure of the data sent is:
```
# data series 1
[
[argument 1]
[argument 2]
[...]
[argument n-1]
[argument n]
]
# data series 2
[
[value 1]
[value 2]
[...]
[value n-1]
[value n]
]
```
where `argument` is x-axis value, `value` is y-axis value and `n` is the ammount of available data.

### _double-column data receiving mode_
A natural evolution of the _single-column data receiving mode_ is providing the server with columns of arguments and data simultaniously. The expected structure of data sent is:
```
# data series 1
[
[argument 1,value 1]
[argument 2,value 2]
[...]
[argument n-1,value n-1]
[argument n,value n]
]
```
where `argument` is x-axis value, `value` is y-axis value and `n` is the ammount of available data.

### _multiple-column data receiving mode_
In order to further accelerate data transfer bewteen the original program and the server, a multiple column transfer approach was implemented. The expected structure of the data sent is:
```
# data series 1
[
[argument 1'a,value 1'a,argument 1'b,value 1'b,...]
[argument 2'a,value 2'a,argument 2'b,value 2'b,...]
[...]
[argument n-1'a,value n-1'a,argument n-1'b,value n-1'b,...]
[argument n'a,value n'a,argument n'b,value n'b,...]
]
```
where `argument` is x-axis value, `value` is y-axis value, `n` is the ammount of available data and `a` and `b` are available data sets.

## Example of C++ implementation
In order to use the matgrapher library with software written in other languages, a UDP socket must be created. The library provides a C++ 11 compatible implementation of of python-C++ interface.

An example code is shown below. This program downloads two sets of data from `file1.txt` and `file2.csv`, runs the built-in python matgrapher gate, sends the downloaded sets to the server and generates a graph. 

```C++
#include <vector>
#include <chrono>
#include <thread>
#include <string>

#include "matgraphergate.h"

#define SERVER "127.0.0.1" // server address (doesn't have to be local)
#define PORT 50553 // server port number
#define MAXLINE 1024 // max length of packet buffer

int main(){
  std::vector<std::vector<double>> fcontents0, fcontents1; // vectors of read file contents
  matgraphergate gr(PORT, SERVER, MAXLINE);// initialise the gate
  
  //loading files
  //arguments for readFile function:
  //-> file to path
  //-> vector to which the data should be saved
  //-> number of ending line (no boundary set if set to 0)
  
  gr.readFile("input/file1.txt", fcontents0, 0);
  gr.split_char = ',';// if a loaded file has a separator different than ' ', than split_char variable must be changed to an appropriate character
  gr.readFile("input/file2.csv", fcontents1, 0);
  
  //automatically running the server
  system("start python -m matgrapher");
  std::this_thread::sleep_for(std::chrono::seconds(2));// unfortunatelly, it takes some time before the server is initialised.
  //preparing internal variables
  gr.sendCommand("echo on");// show debugging messages. Invoke "echo off" to disable.
  std::vector<std::string> labels = {"file 1", "file 2"};// labels used in graph.
  gr.loadLabels(labels, (int)labels.size());// load the labels/
  gr.setExportMethod(1);// show, don't save
  gr.setAxisNames("time [s]", "pressure [Pa]");// set x-axis and y-axis names
  gr.setTitle("Comparison of pressures in time");// set title
  gr.sendCommand("echo off");// disable debugging messages to hide loaded data
  
  //sending data
  std::vector<std::vector<double>> combined_arguments = {fcontents0.at(1), fcontents1.at(1)};//load arguments from column 1 of file1 and file2
  std::vector<std::vector<double>> combined_data = {fcontents0.at(5), fcontents1.at(3)};//load values from column 5 of file1 and from column 3 of file2
  gr.loadMulData(combined_arguments, combined_data);//load data quickly
  std::this_thread::sleep_for(std::chrono::milliseconds(500));// wait for half a second, just to ensure no data gets lost
  
  //creating the graph and cleaning up
  gr.sendCommand("generate graph");// build graph and show it
  gr.sendCommand("destroy graph");// clear internal tables
  gr.sendCommand("end listening");// shut down the server
  
  return 0;
}
```
