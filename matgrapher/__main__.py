#__main__.py

import socket
import grapher

gr = grapher.grapher()
index = 0

def loaddata(data, dt_buffer, hold=True):
    global gr
    global index
    if(b'index' in data):
        index = int(data[-1])-48# 48 wynika z indeksu liczby 0 w tabeli ASCII
        print(index)
    else:
        if(hold == True):
            dt_buffer[index].append(float(data))
        else:
            print(dt_buffer)
            gr.loadData(dt_buffer[0], dt_buffer[1])
            dt_buffer[0].clear()
            dt_buffer[1].clear()
    return dt_buffer

def loadlabels(data, lb_buffer, hold=True):
    global gr
    global index
    if(hold == True):
        lb_buffer.append(str(data))
    else:
        print(lb_buffer)
        gr.loadLabels(lb_buffer)
        lb_buffer.clear()
    return lb_buffer

UDP_IP_ADDRESS = "127.0.0.1"# self udp address
UDP_PORT_NO = 50553# port for communication

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

dt_buffer = [[], []]
lb_buffer = []

loaddata_flag = False
loadlabels_flag = False
settitle_flag = False
setaxisnames_flag = False
setexportmethod_flag = False
setgridvisibility_flag = False
setlogscale_flag = False

while(True):
    data, addr = serverSock.recvfrom(1024)
    if(settitle_flag == True):
        gr.setGraphTitle(str(data))
        settitle_flag = False
    if(setaxisnames_flag == True):
        gr.setAxisNames(str(data).split(',')[0], str(data).split(',')[1])
        setaxisnames_flag = False
    if(setexportmethod_flag == True):
        gr.setExportMethod(int(data)-48)
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
    if(data==b'load data'):
        loaddata_flag = True
    if(data==b'end load data'):
        loaddata_flag = False
        loaddata(b'0', dt_buffer, hold=False)
    if(data==b'load labels'):
        loadlabels_flag = True
    if(data==b'end load labels'):
        loadlabels_flag = False
        loadlabels(b'0', dt_buffer, hold=False)
    if(data==b'generate graph'):
        gr.generateGraph(show=True, save=False)
    if(data==b'set title'):
        settitle_flag = True
    if(data==b'set axisnames'):
        settitle_flag = True
    if(data==b'set exportmethod'):
        settitle_flag = True
    if(data==b'set gridvisibility'):
        settitle_flag = True
    if(data==b'set logscalemethod'):
        settitle_flag = True
    if(data==b'destroy graph'):
        gr.destroyGraphTable()
    if(data==b'end listening'):
        gr.destroyGraphTable()
        break
    print("Message: "+str(data))
    if(loaddata_flag == True and data!=b'load data'):
        dt_buffer = loaddata(data, dt_buffer)
    if(loadlabels_flag == True and data!=b'load labels'):
        lb_buffer = loadlabels(data, lb_buffer)
