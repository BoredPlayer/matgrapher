#__main__.py

import socket
from matgrapher import grapher

gr = None
less_info = True

def loaddata(data, dt_buffer, hold=True):
    global gr
    global index
    if(b'index' in data):
        index = int(data[-1])-48# 48 wynika z indeksu liczby 0 w tabeli ASCII
        if(not less_info):
            print(index)
    else:
        if(hold == True):
            dt_buffer[index].append(float(data))
        else:
            if(not less_info):
                print(dt_buffer)
            gr.loadData(dt_buffer[0], dt_buffer[1])
            dt_buffer[0].clear()
            dt_buffer[1].clear()
    return dt_buffer

def loaddataargs(data, dt_buffer, hold=True):
    global gr
    ln = data.decode().split(",")
    if(hold == True):
        dt_buffer[0].append(float(ln[0]))
        dt_buffer[1].append(float(ln[1]))
        #print(dt_buffer[0][-1])
    else:
        #if(not less_info):
            #print(dt_buffer)
        gr.loadData(dt_buffer[0], dt_buffer[1])
        dt_buffer[0].clear()
        dt_buffer[1].clear()
    return dt_buffer

def loadmuldata(data, array, hold=True):
    '''
    Loads multiple columns of data simulatniously. If held, it will append provided array with new lines of data. Please provide data arguments and values in pairs according to grapher.loadData() documentation:
    [[arguments (float)], [values(float)], ...]
    Arguments:
    -> data (string) - byte string of data provided via communication protocol,
    -> array (float*, ...) - array of floats, provided to matgrapher's internal arrays of data,
    -> hold (boolean) - flag providing information if new data is expected. If true, it will append privided array with arguments and values read from data string.
    Returns:
    -> array (float*, ...) - provided array, expanded with provided data.
    '''
    global gr
    if(hold==True):
        ln = data.decode().split(",")
        if(len(array)<len(ln)):
            for i in range(len(ln)-len(array)):
                array.append([])
        for i in range(len(ln)):
            array[i].append(float(ln[i]))
    else:
        for i in range(int(len(array)/2)):
            gr.loadData(array[2*i], array[2*i+1])
            array[2*i].clear()
            array[2*i+1].clear()
    return array

def loadlabels(data, lb_buffer, hold=True):
    global gr
    global index
    if(hold == True):
        lb_buffer.append(str(data.decode()))
    else:
        if(not less_info):
            print(lb_buffer)
        for i in range(len(lb_buffer)):
            gr.loadLabels(str(lb_buffer[i]))
        lb_buffer.clear()
    return lb_buffer

def main():
    global gr
    global less_info
    gr = grapher.grapher()
    index = 0

    UDP_IP_ADDRESS = "127.0.0.1"# self udp address
    UDP_PORT_NO = 50553# port for communication

    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

    dt_buffer = [[], []]
    lb_buffer = []

    loaddata_flag = False
    loaddataargs_flag = False
    loadmuldata_flag = False
    loadlabels_flag = False
    settitle_flag = False
    setaxisnames_flag = False
    setxlims_flag = False
    setylims_flag = False
    setexportmethod_flag = False
    setfilename_flag = False
    setgridvisibility_flag = False
    setlogscale_flag = False

    graphTitle = gr.graphTitle
    axisNames = gr.axisNames
    exportmethod_save = False
    exportmethod_show = True
    gridvisibility = gr.showGrid    

    print("Margrapher module on.")
    print(f"Waiting for connection @ {UDP_IP_ADDRESS}:{UDP_PORT_NO}\n")

    while(True):
        data, addr = serverSock.recvfrom(1024)
        if(settitle_flag == True):
            if(not less_info):
                print(f"Setting graph title to: {data.decode()}")
            gr.setGraphTitle(str(data.decode()))
            graphTitle = data.decode()
            settitle_flag = False
        if(setfilename_flag == True):
            gr.outputFilename = str(data.decode())
            setfilename_flag = False
        if(setaxisnames_flag == True):
            if(not less_info):
                print("Changing axis names.")
            gr.setAxisNames(str(data).split(',')[0], str(data).split(',')[1][:-1])
            axisNames = data.decode().split(',')[0], str(data).split(',')[1]
            setaxisnames_flag = False
        if(setxlims_flag == True):
            if(not less_info):
                print("Changing X axis range.")
            gr.xlim = [float(data.decode().split(',')[0]), float(str(data).split(',')[1][:-1])]
            setxlims_flag = False
        if(setylims_flag == True):
            if(not less_info):
                print("Changing Y axis range.")
            gr.ylim = [float(data.decode().split(',')[0]), float(str(data).split(',')[1][:-1])]
            setylims_flag = False
        if(setexportmethod_flag == True):
            exportmethod = data.decode()
            if(exportmethod=='0'):
                exportmethod_save = True
                exportmethod_show = False
                exportmethod = 0
                if(not less_info):
                    print("Saving, not showing")
            else:
                exportmethod_save = False
                exportmethod_show = True
                exportmethod = 1
                if(not less_info):
                    print("Showing, not saving")
            gr.setExportMethod(exportmethod)
            setexportmethod_flag = False
        if(setgridvisibility_flag == True):
            if(data==b'True' or data==b'true' or data==b'1'):
                gr.setGridVisibility(true)
            if(data==b'False' or data==b'false' or data==b'0'):
                gr.setGridVisibility(true)
            setgridvisibility_flag = False
        if(setlogscale_flag == True):
            gr.setLogsaceMethod(str(data))
            setlogscale_flag = False
        if(data==b'echo off'):
            less_info = True
        if(data==b'echo on'):
            less_info = False
        if(data==b'load data'):
            loaddata_flag = True
        if(data==b'load dataargs'):
            loaddataargs_flag = True
        if(data==b'load muldata'):
            loadmuldata_flag = True
        if(data==b'end load data'):
            loaddata_flag = False
            loaddata(b'0', dt_buffer, hold=False)
        if(data==b'end load dataargs'):
            loaddataargs_flag = False
            loaddataargs(b'0,0', dt_buffer, hold=False)
        if(data==b'end load muldata'):
            loadmuldata_flag = False
            loadmuldata(b'0,0', dt_buffer, hold=False)
        if(data==b'load labels'):
            loadlabels_flag = True
        if(data==b'end load labels'):
            loadlabels_flag = False
            loadlabels(b'0', lb_buffer, hold=False)
        if(data==b'generate graph'):
            gr.generateGraph(graph_title=graphTitle, axis_names=axisNames, save = exportmethod_save, show = exportmethod_show)
        if(data==b'set title'):
            settitle_flag = True
        if(data==b'set axisnames'):
            setaxisnames_flag = True
        if(data==b'set xlims'):
            setxlims_flag = True
        if(data==b'set ylims'):
            setylims_flag = True
        if(data==b'set exportmethod'):
            setexportmethod_flag = True
        if(data==b'set gridvisibility'):
            setgridvisibility_flag = True
        if(data==b'set logscalemethod'):
            setlogscale_flag = True
        if(data==b'set filename'):
            setfilename_flag = True
        if(data==b'destroy graph'):
            gr.destroyGraphTable()
            dt_buffer = [[], []]
            lb_buffer = []
        if(data==b'end listening'):
            gr.destroyGraphTable()
            break
        if(not less_info):
            print("Message: "+str(data))
        if(loaddata_flag == True and data!=b'load data'):
            dt_buffer = loaddata(data, dt_buffer)
        if(loaddataargs_flag == True and data!=b'load dataargs'):
            dt_buffer = loaddataargs(data, dt_buffer)
        if(loadmuldata_flag == True and data!=b'load muldata'):
            dt_buffer = loadmuldata(data, dt_buffer)
        if(loadlabels_flag == True and data!=b'load labels'):
            lb_buffer = loadlabels(data, lb_buffer)
    return None

if __name__=="__main__":
    main()
