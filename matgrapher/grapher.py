import matplotlib
import matplotlib.pyplot as plt
import warnings

class grapher(object):
    """
    A simple class covering typical use of generating graphs.
    Exmple of usage:
    0) import class by using    "from matgrapher import grapher"
    1) create new object i.e.   "gr = grapher.grapher()"
    2) load labels              "gr.loadLabels(label1, label2)"
    3) load data                "gr.loadData(x_data1, y_data1, x_data2, y_data2)"
    4) generate graph           "gr.generateGraph()"
    5) remove loaded data       "gr.destroyGraphTable()"
    """

    x_table = []
    y_table = []
    labels = []
    xlim = []
    ylim = []
    graphTitle = "Graph"
    axisNames = ["X Values", "Y Values"]
    outputFilename = "output/file.png"
    dpi = 300
    plotSize = [15*1.5/2.54, 15*1.5/2.54]
    showGrid = True
    saveFile = True
    showFigure = False
    logscale = 'none'

    def __init__(self):
        pass

    def destroyGraphTable(self):
        '''
        Clean all data provided.
        '''
        for i in range(len(self.x_table)):
            del self.x_table[0]
        for i in range(len(self.y_table)):
            del self.y_table[0]
        for i in range(len(self.labels)):
            del self.labels[0]
        return None

    def loadLabels(self, label, *args):
        '''
        Load labels to internal array. Please provide them in order as x, y arguments were provided.
        Arguments:
        -> label (string) - label used in legend to describe a dataset,
        -> *args (string, ...) - following labels if needed to load more than one in one step
        '''
        if(len(self.labels)+len(args)+1<len(self.x_table)):
            warnings.warn(f"Not all data sets ({len(self.x_table)}) are labeled.")

        self.labels.append(label)
        if(len(args)>0):
            for i in range(len(args)):
                self.labels.append(args[i])

    def loadData(self, x_argument, y_argument, *args):
        '''
        Load data to internal tables. Please provide it in pairs [x1, y1, x2, y2, ...]
        Arguments:
        -> x_argument ([float, ...]) - one dimensional array of x axis values,
        -> y_argument ([float, ...]) - one dimensional array of y axis values.
        '''
        if(len(args)%2!=0):
            warnings.warn(f"Expected equal ammount of x and y data sets. Got ({int((len(args)+1)/2)}) and ({int((len(args)-1)/2)}).")

        self.x_table.append(x_argument.copy())
        self.y_table.append(y_argument.copy())
        if(len(args)>0):
            for i in range(int(len(args)/2)):
                self.x_table.append(args[2*i])
                self.y_table.append(args[2*i+1])
    
    def setAxisNames(self, X_axis, Y_axis):
        self.axisNames = [X_axis, Y_axis]
        
    def setGraphTitle(self, graph_title):
        self.graphTitle = graph_title
    
    def setFilename(self, filename):
        self.outputFilename = filename
        
    def setExportMethod(self, method):
        '''
        Sets method of exporting file.
        0 - save, don't show
        1 - don't save, show
        2 - save and show
        '''
        if(method!=0 and method!=1 and method!=2):
            warnings.warn(f"Warning: wrong export method provided: {method}. Falling back to method 1 (don't save, show)")
        if(method==0):
            self.saveFile = True
            self.showFigure = False
        if(method==1):
            self.saveFile = False
            self.showFigure = True
        if(method==2):
            self.saveFile = True
            self.showFigure = True
    
    def setGridVisibility(self, grid_visible):
        self.showGrid = grid_visible
    
    def setLogscaleMethod(self, logscale_method):
        self.logscale = logscale_method

    def generateGraph(self, data_x=x_table, data_y=y_table, axis_names=axisNames, x_lim = xlim, y_lim = ylim, graph_title=graphTitle, legend=labels, filename=outputFilename, dpi=dpi, plot_size = plotSize , grid = showGrid, save=saveFile, show=showFigure, tight_layout=True, log_scale = logscale):
        '''
        Draw a graph based on provided data.
        Arguments:
        -> data_x ([float, ...]) - data shown as argument X of the drawn chart,
        -> data_y ([float, ...]) - data shown as argument Y of the drawn chart,
        -> axis_names ([string, string]) - table of axis names ([0] - X axis, [1] - Y axis]),
        -> x_lim ([float, float]) - limits of x_axis (if an empty array is passed (default), no limits are imposed)
        -> y_lim ([float, float]) - limits of y_axis (if an empty array is passed (default), no limits are imposed)
        -> graph_title (string) - a title for drawn graph,
        -> legend ([string, ...]) - tabe of labels used in legend,
        -> filename (string) - name for the output file,
        -> dpi (int) - Dots Per Inch (resolution) of the exported graph,
        -> plot_size ([float, float]) - size of the exported graph (in inches - conversion ratio cm->inch is 1/2.54),
        -> grid (boolean) - argument for generating grid in the drawn graph
        -> save (boolean) - flag for saving drawn graph
        -> show (boolean) - flag for showing drawn graph
        '''
        lx = len(data_x)
        ly = len(data_y)
        if(lx!=ly):
            raise Exception(f"Error: Expected equal length of data_x ({lx}) and data_y ({ly}) arrays.")
        if(lx>len(legend) and len(legend)!=0):
            warnings.warn("Warning: Not all provided data has been assigned with legend label.")
        if(lx<len(legend)):
            warnings.warn("Warning: Provided more labels than data.")
    
        plt.figure(figsize = (plot_size[0], plot_size[1]))
        for data_set_index, (xd, yd) in enumerate(zip(data_x, data_y)):
            if(data_set_index>=len(legend)):
                plt.plot(xd, yd)
            else:
                plt.plot(xd, yd, label = legend[data_set_index])
        if(len(legend)>0):
            plt.legend()
        plt.xlabel(axis_names[0])
        plt.ylabel(axis_names[1])
        plt.title(graph_title)
        plt.grid(grid)
        if(len(x_lim)==2):
            plt.xlim(x_lim[0], x_lim[1])
        if(len(y_lim)==2):
            plt.ylim(y_lim[0], y_lim[1])
        if(log_scale=='y'):
            plt.yscale('log')
        if(log_scale=='x'):
            plt.xscale('log')
        if(log_scale=='xy'):
            plt.yscale('log')
            plt.xscale('log')
        if(save):
            if(tight_layout):
                plt.savefig(filename, bbox_inches='tight')
            else:
                plt.savefig(filename)
        if(show):
            plt.show()
        plt.close()
