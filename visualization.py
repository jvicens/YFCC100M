__author__ = 'julian'

import plotly.plotly as py
import plotly.graph_objs as go

import csv
import sys

def scatter_plot(file, type):

    latitudes = []
    longitudes = []
    accumulate = []

    f = open(file, 'rb')
    try:
        reader = csv.reader(f)
        for row in reader:
            latitudes.append(row[0])
            longitudes.append(row[1])
            accumulate.append(row[2])


    finally:
        f.close()

    data = [
        go.Heatmap(
            z=[latitudes,
               longitudes,
               accumulate]
        )
    ]
    #plot_url = py.plot(data, filename="bcn_"+type)