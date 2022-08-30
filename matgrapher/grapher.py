import matplotlib
import matplotlib.pyplot as plt
import numpy as np
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

    def __init__(self):
        self.x_table = []
        self.y_table = []
        self.contour_plots = []
        self.point_table = [[], []]# x, y
        self.point_colors = [[], []]# color (in hex or matplotlib), alpha
        self.point_sizes = []
        self.point_alpha_change = []
        self.text_table = [[], []]
        self.labels = []
        self.xlim = []
        self.ylim = []
        self.linestyle = []
        self.colors = []
        self.show_label = []
        self.line_widths = []
        self.default_width = 1.3
        self.graphTitle = "Graph"
        self.axisNames = ["X Values", "Y Values"]
        self.outputFilename = "output/file.png"
        self.dpi = 300
        self.plotSize = [15*1.5/2.54, 15*1.5/2.54]
        self.showGrid = True
        self.saveFile = True
        self.showFigure = False
        self.logscale = 'none'

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
        for i in range(len(self.linestyle)):
            del self.linestyle[0]
        for i in range(len(self.colors)):
            del self.colors[0]
        for i in range(len(self.point_table[0])):
            del self.point_table[0][0]
            del self.point_table[1][0]
        for i in range(len(self.point_colors[0])):
            del self.point_colors[0][0]
            del self.point_colors[1][0]
        for i in range(len(self.point_sizes)):
            del self.point_sizes[0]
        for i in range(len(self.point_alpha_change)):
            del self.point_alpha_change[0]
        for i in range(len(self.contour_plots)):
            del self.contour_plots[0]
        for i in range(len(self.text_table[0])):
            del self.text_table[0][0]
            del self.text_table[1][0]
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
        self.show_label.append(True)
        if(len(args)>0):
            for i in range(len(args)):
                self.labels.append(args[i])
                self.show_label.append(True)

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

        self.line_widths.append(self.default_width)
                
    def createContourPlot(self, fn, xlist, ylist):
        X, Y = np.meshgrid(xlist, ylist)
        Z = fn(X, Y)
        contour = [X, Y, Z]
        self.contour_plots.append(contour)
    
    def loadPoints(self, point, *args):
        '''
        Load points to internal table.
        If you wish to enable autocoloring of points, add "autocolor:[color of the point set],[opacity level]" string at the end of arguments.
        If opacity level is not provided, it will be assumed as 1.0.
        Arguments:
        -> point ([float, float]) - list containing point coordinates.
        '''
        autocolor_flag = False
        size_flag = False
        command_line = None #a command line at the end of arguments
        last_alpha = 0.0
        if(len(self.point_colors[1])>0):
            last_alpha = self.point_colors[1][-1]
        if(not isinstance(point[0], list) and not isinstance(point[0], np.ndarray)):
            self.point_table[0].append(point[0])
            self.point_table[1].append(point[1])
        else:
            if(len(point[0])!=len(point[1])):
                warnings.warn("Warning! Point data columns not equal in length! Not all points may be included.")
            for i in range(min([len(point[0]), len(point[1])])):
                self.point_table[0].append(point[0][i])
                self.point_table[1].append(point[1][i])
        if(len(args)>0):
            #check for command line at the end of arguments
            if(type(args[-1])==str):
                command_line = args[-1].split(";")
            #check for autocolor at the end of args
            for cmd in command_line:
                #if 'size' option is enabled
                if('size' in cmd):
                    size = cmd.split(":")[-1]
                    try:
                        size = float(size)
                    except:
                        size = 20.0# autosizing, if user fails to provide correct size
                    if(isinstance(point[0], list) or isinstance(point[0], np.ndarray)):
                        for i in range(min([len(point[0]), len(point[1])])):
                            self.point_sizes.append(size)
                    else:
                        self.point_sizes.append(size)
                    size_flag = True
                #if 'autocolor' option is enabled
                if('autocolor' in cmd):
                    color = cmd.split(":")[-1]#remove 'autocolor' from the argument
                    # fixing autocolor string
                    if(color == '' or color == 'autocolor'):# if user forgot to add color after autocolor
                        color = '#4e4e4e,1.0'
                    elif('autocolor' in color):#if 'autcolor' could not be removed (user forgot to add ':')
                        color = color.split("autocolor")[-1]# remove 'autocolor' forcefully
                    else:
                        # checking if user stated opacity correctly
                        try:
                            float(color.split(',')[-1])
                        except:
                            color = color.split(',')[0]+',1.0'
                    autocolor_flag = True
                    #colouring if the basic argument were list
                    if(isinstance(point[0], list) or isinstance(point[0], np.ndarray)):
                        for i in range(min([len(point[0]), len(point[1])])):
                            self.point_colors[0].append(color.split(',')[0])
                            self.point_colors[1].append(float(color.split(',')[1]))
                            if(last_alpha!=self.point_colors[1][-1]):
                                self.point_alpha_change.append(len(self.point_colors[1])-1)
                                last_alpha = self.point_colors[1][-1]
                    else:
                        self.point_colors[0].append(color.split(',')[0])
                        self.point_colors[1].append(float(color.split(',')[1]))
                        if(last_alpha!=self.point_colors[1][-1]):
                            self.point_alpha_change.append(len(self.point_colors[1])-1)
                            last_alpha = self.point_colors[1][-1]
            if(size_flag == False):
                if(isinstance(point[0], list) or isinstance(point[0], np.ndarray)):
                    for i in range(min([len(point[0]), len(point[1])])):
                        self.point_sizes.append(20.0)
                else:
                    self.point_sizes.append(20.0)
            #add additional points defined in the arguments
            for i in range(len(args)):
                if(autocolor_flag == True):
                    if(i == len(args)-1):
                        break
                    self.point_colors[0].append(color.split(',')[0])
                    self.point_colors[1].append(float(color.split(',')[1]))
                if(size_flag==True):
                    self.point_sizes.append(size)
                if(size_flag==False):
                    self.point_sizes.append(20.0)
                self.point_table[0].append(args[i][0])
                self.point_table[1].append(args[i][1])
    
    def changePointColor(self, color, point_index, end_point_index = None):
        '''
        Change color of a point or set of points in internal tables. If the point index is uknown, provide its position in form of a list.
        Arguments:
        -> color (string) - color of the point,
        -> point_index (int or [float, float]) - index number or position of the point,
        -> end_point_index (int or [float, float]) - index number or position of the last point of the set.
        '''
        if(isinstance(point_index, list)):
            pos = [var for var, val in enumerate(zip(self.point_table[0], self.point_table[1])) if val[0]==point_index[0] and val[1]==point_index[1]]
            for p in pos:
                self.point_colors[p] = color
            if(end_point_index != None):
                if(isinstance(end_point_index, list)):
                    end_pos = [var for var, val in enumerate(zip(self.point_table[0], self.point_table[1])) if val[0]==end_point_index[0] and val[1]==end_point_index[1]]
                    for i in range(min(pos), max(end_pos)):
                        self.point_colors[i] = color
                else:
                    for i in range(min(pos), end_point_index):
                        self.point_colors[i] = color
        else:
            self.point_colors[point_index] = color
            if(end_point_index != None):
                if(isinstance(end_point_index, list)):
                    end_pos = [var for var, val in enumerate(zip(self.point_table[0], self.point_table[1])) if val[0]==end_point_index[0] and val[1]==end_point_index[1]]
                    for i in range(point_index, max(end_pos)):
                        self.point_colors[i] = color
                else:
                    for i in range(point_index, end_point_index):
                        self.point_colors[i] = color

    def setPointColor(self, color, alpha = 1.0):
        '''
        Set color and transparency of a point.
        Arguments:
        -> color (string) - color of the point,
        -> alpha (float) - level of point transparency (between 0.0 and 1.0).
        '''
        self.point_colors[0].append(color)
        self.point_colors[1].append(alpha)

    def loadText(self, text, position, *args):
        '''
        Load positioned text into internal table. Please provide arguments in pairs of text1, position1, text2, position2, ...
        Arguments:
        -> text (string) - string to be displayed
        -> point ([float, float]) - list containing text position
        '''
        if(len(args)%2==1):
            warnings.warn(f"Warning! Data pairing (text, position) not complete. Expected even ammount of arguments, got odd. Last point will be set to [0.0, 0.0]")
        self.text_table[0].append(text)
        self.text_table[1].append(position)
        if(len(args)>0):
            for i in range(int(len(args)/2)):
                if(not isinstance(args[2*i+1], list)):
                    warnings.warn("Warning! Wrong data type provided! Expected position as list, got "+str(type(args[2*i+1]))+". Aborting loading text.")
                    return None
                self.text_table[0].append(args[2*i])
                self.text_table[1].append(args[2*i+1])
            if(i*2<len(args)-1 and i!=0):
                self.text_table[0].append(args[-1])
                self.text_table[1].append([0.0, 0.0])
                
    def hideLabel(self, label_index=False, label=''):
        '''
        Hide label from graph legend.
        Arguments:
        -> label_index (int or bool) - index of label to be hidden. Assign 'False' if more than one label is to be hidden.
        -> label (string) - label or labels to be hidden if share the same text.
        '''
        if(label!=''):
            if(label in self.labels):
                for i in range(len(self.labels)):
                    if(self.labels[i]==label):
                        self.show_label[i]=False
            else:
                warning.warn(f"Warning: No label {label} found!")
        else:
            if(label_index!=False):
                try:
                    self.show_label[label_index] = False
                except:
                    warning.warn(f"Warning: Could not hide label {label_index}. Size of label array is {len(self.show_label)}")

    def changeDefaultWidth(self, width):
        if(isintance(width, float) or isinstance(width, int)):
            self.default_width = width
        else:
            warnings.warn(f"Warning: Expected width type of float or int not ({type(width)})")

    def changeLineWidth(self, width, index=None):
        if(not isinstance(width, float) and not isinstance(width, int)):
            warnings.warn(f"Warning: Expected float or int value, not {type(width)} as line width.\nLine width will not be changed.")
            return
        if(isinstance(index, int)):
            if(index>len(self.line_widths)):
                warnings.warn(f"Warning: Requesting higher index ({index}) than length of the array ({len(self.line_widths)}).\nFalling back to max available index")
                index = len(self.line_widths)-1
            try:
                self.line_widths[index] = width
            except:
                warnings.warn(f"Warning: Could not change selected line width (@ line: {index})")
        if(index==None):
            try:
                self.line_widths[-1] = width
            except:
                warnings.warn(f"Warning: Could not change selected line width.\tPerhaps there is no data in arrays?")
        if(isinstance(index, list)):
            if(len(index)>len(line_widths)):
                warnings.warn(f"Warning: Index array longer than data array!\nExpected at most {len(self.line_widths)} widths, got {len(index)}.\nUpdating only available data.")
            try:
                for i in range(min(len(index), len(self.len_widths))):
                    self.line_widths[index[i]] = width
            except:
                warnings.warn("Warning: could not edit line width.")
        if(isinstance(index, np.ndarray)):
            if(index.ndim>1):
                warnigns.warn(f"Warning: Expected 1D numpy array, got {index.ndim}D array.")
                return
            if(len(index)>len(self.line_widths)):
                warnings.warn(f"Warning: Index array longer than data array!\nExpected at most {len(self.line_widths)} widths, got {len(index)}.\nUpdating only available data.")
            try:
                for i in range(min(len(index), len(self.len_widths))):
                    self.line_widths[index[i]] = width
            except:
                warnings.warn("Warning: could not edit line width.")
            
    
    def loadLineStyles(self, linestyle, *args):
        self.linestyle.append(linestyle)
        if(len(args)>0):
            for i in range(len(args)):
                self.linestyle.append(args[i])
    
    def changeLineStyle(self, index, newlinestyle, linestyle = '-'):
        if(index == 'u'):
            if(linestyle in self.linestyle):
                for i in range(len(self.linestyle)):
                    if(self.linestyle==linestyle):
                        self.linestyle = newlinestyle
        self.linestyle[index] = newlinestyle
    
    def loadColor(self, color, *args):
        self.colors.append(color)
        if(len(args)>0):
            for cl in args:
                self.colors.append(cl)
    
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

    def generateGraph(self,
                        data_x=None,
                        data_y=None,
                        axis_names=None,
                        x_lim = None,
                        y_lim = None,
                        graph_title=None,
                        line_styles=None,
                        line_widths=None,
                        colors = None,
                        legend=None,
                        legend_args = '',
                        legend_position = '',
                        filename=None,
                        dpi=None,
                        plot_size = None,
                        grid = None,
                        save=None,
                        show=None,
                        tight_layout=True,
                        log_scale = None ):
        '''
        Draw a graph based on provided data.
        Arguments:
        -> data_x ([float, ...]) - data shown as argument X of the drawn chart,
        -> data_y ([float, ...]) - data shown as argument Y of the drawn chart,
        -> axis_names ([string, string]) - table of axis names ([0] - X axis, [1] - Y axis]),
        -> x_lim ([float, float]) - limits of x_axis (if an empty array is passed (default), no limits are imposed)
        -> y_lim ([float, float]) - limits of y_axis (if an empty array is passed (default), no limits are imposed)
        -> graph_title (string) - a title for drawn graph,
        -> line_styles ([string, ...]) - line styles as matplotlib argument
        -> line_widths ([float, ...]) - widths of the drawn lines
        -> colors ([string, ...]) - line colors as matplotlib argument
        -> legend ([string, ...]) - tabe of labels used in legend,
        -> legend_args (string) - arguments for plt.legend function
        -> legend_position (string) - argument for legend location as matplotlib argument
        -> filename (string) - name for the output file,
        -> dpi (int) - Dots Per Inch (resolution) of the exported graph,
        -> plot_size ([float, float]) - size of the exported graph (in inches - conversion ratio cm->inch is 1/2.54),
        -> grid (boolean) - argument for generating grid in the drawn graph
        -> save (boolean) - flag for saving drawn graph
        -> show (boolean) - flag for showing drawn graph
        -> tight_layout (boolean) - flag for enabling/disabling tight layout of the graph (default: True)
        -> log_scale (string) - settings for log scale at chosen axis
        '''
        #initializing graph arguments
        if(data_x == None):
            data_x = self.x_table
        if(data_y == None):
            data_y = self.y_table
        if(axis_names == None):
            axis_names = self.axisNames
        if(x_lim == None):
            x_lim = self.xlim
        if(y_lim == None):
            y_lim = self.ylim
        if(graph_title == None):
            graph_title = self.graphTitle
        if(line_styles == None):
            line_styles = self.linestyle
        if(line_widths == None):
            line_widths = self.line_widths
        if(colors == None):
            colors = self.colors
        if(legend == None):
            legend = self.labels
        if(filename == None):
            filename = self.outputFilename
        if(dpi == None):
            dpi = self.dpi
        if(plot_size == None):
            plot_size = self.plotSize
        if(grid == None):
            grid = self.showGrid
        if(save == None):
            save = self.saveFile
        if(show == None):
            show = self.showFigure
        if(log_scale == None):
            log_scale = self.logscale

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
            if(data_set_index>=len(legend) or self.show_label[data_set_index]==False):
                if(data_set_index>=len(line_styles)):
                    if(data_set_index>=len(colors)):
                        plt.plot(xd, yd, linewidth=line_widths[data_set_index])
                    else:
                        plt.plot(xd, yd, colors[data_set_index], linewidth=line_widths[data_set_index])
                else:
                    if(data_set_index>=len(colors)):
                        plt.plot(xd, yd, linestyle=line_styles[data_set_index], linewidth=line_widths[data_set_index])
                    else:
                        plt.plot(xd, yd, linestyle=line_styles[data_set_index], color=colors[data_set_index], linewidth=line_widths[data_set_index])
            else:
                if(data_set_index>=len(line_styles)):
                    if(data_set_index>=len(colors)):
                        plt.plot(xd, yd, label = legend[data_set_index], linewidth=line_widths[data_set_index])
                    else:
                        plt.plot(xd, yd, label = legend[data_set_index], color=colors[data_set_index], linewidth=line_widths[data_set_index])
                else:
                    if(data_set_index>=len(colors)):
                        plt.plot(xd, yd, label = legend[data_set_index], linestyle=line_styles[data_set_index], linewidth=line_widths[data_set_index])
                    else:
                        plt.plot(xd, yd, label = legend[data_set_index], linestyle=line_styles[data_set_index], color=colors[data_set_index], linewidth=line_widths[data_set_index])
        if(len(legend)>0):
            if(legend_args==''):
                if(legend_position==''):
                    plt.legend()
                else:
                    plt.legend(loc=legend_position)
            else:
                if(legend_position==''):
                    plt.legend(legend_args)
                else:
                    plt.legend(legend_args, loc=legend_position)
        
        if(len(self.point_table[0])>0):
            if(len(self.point_colors[0])>0):
                if(len(self.point_sizes)>0):
                    for i in range(len(self.point_alpha_change)-1):
                        plt.scatter(self.point_table[0][self.point_alpha_change[i]:self.point_alpha_change[i+1]], self.point_table[1][self.point_alpha_change[i]:self.point_alpha_change[i+1]], c=self.point_colors[0][self.point_alpha_change[i]:self.point_alpha_change[i+1]], alpha = self.point_colors[1][self.point_alpha_change[i]], s=self.point_sizes[self.point_alpha_change[i]:self.point_alpha_change[i+1]])
                    plt.scatter(self.point_table[0][self.point_alpha_change[-1]:], self.point_table[1][self.point_alpha_change[-1]:], c=self.point_colors[0][self.point_alpha_change[-1]:], alpha = self.point_colors[1][self.point_alpha_change[-1]], s=self.point_sizes[self.point_alpha_change[-1]:])
                else:
                    for i in range(len(self.point_alpha_change)-1):
                        plt.scatter(self.point_table[0][self.point_alpha_change[i]:self.point_alpha_change[i+1]], self.point_table[1][self.point_alpha_change[i]:self.point_alpha_change[i+1]], c=self.point_colors[0][self.point_alpha_change[i]:self.point_alpha_change[i+1]], alpha = self.point_colors[1][self.point_alpha_change[i]])
                    plt.scatter(self.point_table[0][self.point_alpha_change[-1]:], self.point_table[1][self.point_alpha_change[-1]:], c=self.point_colors[0][self.point_alpha_change[-1]:], alpha = self.point_colors[1][self.point_alpha_change[-1]])
            else:
                plt.scatter(self.point_table[0], self.point_table[1])

        if(len(self.text_table)>0):
            for i in range(len(self.text_table[0])):
                plt.text(self.text_table[1][i][0], self.text_table[1][i][1], self.text_table[0][i])

        if(len(self.contour_plots)>0):
            for i in range(len(self.contour_plots)):
                cp = plt.contourf(self.contour_plots[i][0], self.contour_plots[i][1], self.contour_plots[i][2], cmap='coolwarm')
                plt.colorbar(cp)
                #plt.clabel(cp, inline=True)

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
                plt.savefig(filename, bbox_inches='tight', dpi=dpi)
            else:
                plt.savefig(filename, dpi=dpi)
        if(show):
            plt.show()
        plt.close()
