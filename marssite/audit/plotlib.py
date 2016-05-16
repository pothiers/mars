import matplotlib.pyplot as plt
import numpy as np
import io

def write_fig(fig):
    svgbuf = io.StringIO()
    fig.savefig(svgbuf, format='svg')
    svg_data = svgbuf.getvalue() # return in HTTP response
    with open('test.html', 'w') as f:
        f.write(svg_data) 
    print('WROTE: test.html')

# with url.py entry containing png like:
#    (r'^charts/simple.png$', 'myapp.views.charts.simple'),
#! def fig_response(fig):    
#!     canvas = FigureCanvas(fig)
#!     response = HttpResponse(content_type='image/png')
#!     canvas.print_png(response)v
#!     matplotlib.pyplot.close(f)
#!     return response

audit_data=[
    dict(name='mix-1',     D=9,  C=2, B=8),

    dict(name='allval-2',  D=4,  C=1, B=0),
    dict(name='norej-3',   D=6,  C=0, B=3),
    dict(name='noaccep-4', D=0,  C=3, B=5),

    dict(name='novally-5', D=0,  C=0, B=12),  #recieved nada
    dict(name='onlyrej-6', D=0,  C=7, B=0),
    dict(name='onlyacc-7', D=9,  C=0, B=0),
    ]

def hbarplot(countdata):
    #countdata = dict() # data[(tele,inst,day)] = (nosubmit,rejected,accepted)
    daykeys = list(countdata.keys())
    counts = np.array([ list(reversed(countdata[dk])) for dk in daykeys])
    data = counts.transpose() # N x 3 (columns X rows)
    #print('hgbarplot.data={}'.format(data))
    numrows = len(daykeys)
    y_pos = np.arange(numrows)
    heightIn = numrows * .5
    fig = plt.figure(figsize=(10,heightIn))  # w,h (inches)
    ax = fig.add_subplot(111)

    plt.title('Observations per Telescope, Instrument, Day')

    colors ='gyr' # D,C,B
    patch_handles = []
    left = np.zeros(numrows) # left alignment of data starts at zero
    for i, d in enumerate(data):
        patch_handles.append(ax.barh(y_pos, d, 
                                     color=colors[i%len(colors)],
                                     align='center', 
                                     left=left))
        # accumulate the left-hand offsets
        left += d
        
    # go through all of the bar segments and annotate
    for j in range(len(patch_handles)):
        for i, patch in enumerate(patch_handles[j].get_children()):
            bl = patch.get_xy()
            x = 0.5*patch.get_width() + bl[0]
            y = 0.5*patch.get_height() + bl[1]
            if counts[i,j] != 0:
                ax.text(x,y, "%d" % (counts[i,j]), ha='center')
                
    ax.set_yticks(y_pos)
    ax.set_yticklabels(['{}:{}:{}'.format(tele,inst,day)
                        for (tele,inst,day) in daykeys])
    ax.set_xlabel('Number of files')
    #! ax.legend()
    plt.tight_layout()

    svgbuf = io.StringIO()
    fig.savefig(svgbuf, format='svg')
    svg_data = svgbuf.getvalue() # return in HTTP response
    return svg_data
    

def plot():
    #!labels = [d['name'] for d in audit_data]
    #!d_list = [d['D']    for d in audit_data]
    #!c_list = [d['C']    for d in audit_data]
    #!b_list = [d['B']    for d in audit_data]
    counts = np.array([ [di[key] for key in ['D','C','B']]
                      for di in audit_data])  #  3xN
    data = counts.transpose() # N x 3 
    y_pos = np.arange(len(audit_data))

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)

    plt.title('Observations for one day')

    #colors ='rgbwmc'
    colors ='gyr' # D,C,B
    patch_handles = []
    left = np.zeros(len(audit_data)) # left alignment of data starts at zero
    for i, d in enumerate(data):
        patch_handles.append(ax.barh(y_pos, d, 
                                     color=colors[i%len(colors)],
                                     align='center', 
                                     left=left))
        # accumulate the left-hand offsets
        left += d
        
    # go through all of the bar segments and annotate
    for j in range(len(patch_handles)):
        for i, patch in enumerate(patch_handles[j].get_children()):
            bl = patch.get_xy()
            x = 0.5*patch.get_width() + bl[0]
            y = 0.5*patch.get_height() + bl[1]
            if counts[i,j] != 0:
                ax.text(x,y, "%d" % (counts[i,j]), ha='center')
                
    ax.set_yticks(y_pos)
    ax.set_yticklabels([d['name'] for d in audit_data])
    ax.set_xlabel('Number of files')

    #write_fig(fig)
    svgbuf = io.StringIO()
    fig.savefig(svgbuf, format='svg')
    svg_data = svgbuf.getvalue() # return in HTTP response
    return svg_data


##############################################################################
### Just examples below here!!!
###

def plot0():
    import io

    x = np.arange(0,np.pi*3,.1)
    y = np.sin(x)

    fig = plt.figure()
    plt.plot(x,y)

    imgdata = io.StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data
    
    svg_data = imgdata.getvalue() 

    with open('test.html', 'w') as f:
        f.write(svg_data) 
    print('WROTE: test.html')

def plot1():
    "For service to return image of plot"
    pos = arange(10)+ 2 
    barh(pos,(1,2,3,4,5,6,7,8,9,10),align = 'center')

    yticks(pos,('#hcsm','#ukmedlibs','#ImmunoChat','#HCLDR','#ICTD2015','#hpmglobal','#BRCA','#BCSM','#BTSM','#OTalk'))

    xlabel('Popularidad')
    ylabel('Hashtags')
    title('Gráfico de Hashtags')
    subplots_adjust(left=0.21)
    
    buffer = io.BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.fromstring('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    #return HttpResponse (buffer.getvalue(), content_type="Image/png")

def plot2():
    people = ('A','B','C','D','E','F','G','H')
    segments = 4
    
    # generate some multi-dimensional data & arbitrary labels
    data = 3 + 10* np.random.rand(segments, len(people))
    percentages = (np.random.randint(5,20, (len(people), segments)))
    y_pos = np.arange(len(people))
    
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    
    colors ='rgbwmc'
    patch_handles = []
    left = np.zeros(len(people)) # left alignment of data starts at zero
    for i, d in enumerate(data):
        patch_handles.append(ax.barh(y_pos, d, 
                                     color=colors[i%len(colors)],
                                     align='center', 
                                     left=left))
        # accumulate the left-hand offsets
        left += d
        
    # go through all of the bar segments and annotate
    for j in range(len(patch_handles)):
        for i, patch in enumerate(patch_handles[j].get_children()):
            bl = patch.get_xy()
            x = 0.5*patch.get_width() + bl[0]
            y = 0.5*patch.get_height() + bl[1]
            ax.text(x,y, "%d%%" % (percentages[i,j]), ha='center')
                
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.set_xlabel('Distance')

    #plt.show()
    write_fig(fig)
