__author__ = 'julian'


import numpy as np
import pandas as pd
from bokeh.plotting import *
from bokeh.objects import HoverTool, ColumnDataSource

#
########## Load data ##########
#
data_path = '/path/to/data/'
node_file = data_path + '/nodes.csv' # 1 column of node names - header = "name"
link_file = data_path + '/matrix.csv' # raw connectivity matrix - square, no headers


nodes = pd.read_csv(node_file)
# nodes

nodes['name'] = [str(x) for x in nodes['name']]
names = list(nodes['name'])

links_csv = np.loadtxt(open(link_file,"rb"),delimiter=",") # add skiprows=1 if there is a header

#
########## Manipulate data into appropriate format ##########
#
n1 = []
n2 = []
color = []
weight = []
alpha = []
for node1 in range(0,13):
    for node2 in range(0,13):
        n1.append(names[node1])
        # n2.append(str(node1) + " " + names[node2])
        n2.append(names[node2])
        value = links_csv[node1][node2]
        weight.append(value)
        if value < 0:
            color.append('#0066FF')
            alpha.append(value + .2)
        elif value > 0 and value < 1:
            color.append('#B00000')
            alpha.append(value)
        else:
            color.append('#000000')
            alpha.append(value)

# create a `ColumnDataSource` with columns: month, year, color, rate
source = ColumnDataSource(
    data=dict(
        n1=n1,
        n2=n2,
        color=color,
        weight=weight,
        alpha=alpha,
    )
)

########## Output ##########

output_file('brain.html')

figure()

rect('n1', 'n2', 0.9, 0.9, source=source,
     x_range=list(reversed(names)), y_range=names,
     color='color', alpha='alpha', line_color=None,
     tools="resize,hover", title="Brain",
     plot_width=750, plot_height=750)

grid().grid_line_color = None
axis().axis_line_color = None
axis().major_tick_line_color = None
axis().major_label_text_font_size = "5pt"
axis().major_label_standoff = 0
xaxis().location = "above"
xaxis().major_label_orientation = np.pi/3

hover = [t for t in curplot().tools if isinstance(t, HoverTool)][0]
hover.tooltips = OrderedDict([
    ('Nodes', '@n1, @n2'),
    ('Pearsons r', '@weight'),
])

show() # show the plot