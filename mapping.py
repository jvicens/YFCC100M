__author__ = 'julian'

import math
import numpy as np
import pymongo as pm
import csv
from collections import Counter
from itertools import chain, combinations
import unicodedata

'''

p1 = {"latitude":2.3123, "longitude":2.1}
p2 = {"latitude":1.2234, "longitude":3.834543}
p3 = {"latitude":4.8, "longitude":3.4345}
p4 = {"latitude":3.6, "longitude":1.2}
p5 = {"latitude":3.8456, "longitude":1.3}
p6 = {"latitude":1.6456, "longitude":2.3}
p7 = {"latitude":2.8723, "longitude":4.6}
p8 = {"latitude":1.198, "longitude":2.4}
p9 = {"latitude":0.2, "longitude":3.1}

points = []
points.append(p1)
points.append(p2)
points.append(p3)
points.append(p4)
points.append(p5)
points.append(p6)
points.append(p7)
points.append(p8)
points.append(p9)


step = 1

min_lat = 0
min_lon = 0
max_lat = 5 + step
max_lon = 5 + step



latitudes = []
longitudes = []
for i in np.arange(min_lat, max_lat, step):
    latitudes.append(i)
    longitudes.append(i)

points_mapping = []

for point in points:
    for latitude in latitudes:
        if math.fabs(point["latitude"] - latitude) <= step/float(2):
            lan = latitude
    for longitude in longitudes:
        if math.fabs(point["longitude"] - longitude) <= step/float(2):
            lon = longitude

    #p = {"latitude":lan, "longitude":lon}
    p = [lan, lon]
    points_mapping.append(p)

print(points_mapping)


c = Counter(chain.from_iterable(combinations(x,2) for x in points_mapping))
t = c.most_common(len(c))
print(t)

myfile = open('test.csv', 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)


for point in t:

    print(point.__getitem__(0).__getitem__(0))
    print(point.__getitem__(0).__getitem__(1))
    print(point.__getitem__(1))
    wr.writerow(str(point.__getitem__(0).__getitem__(0))+str(point.__getitem__(0).__getitem__(1))+str(point.__getitem__(1)))


'''

'''
MappingAll()

Get all geopoints and save in a .csv
'''

def MappingAll():

    connection = pm.Connection()
    db = connection["YFCC100M"]

    collection_BCN = db.YFCC100M_BCN

    file = open('mapping_all.csv', 'wb')
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)

    for i in collection_BCN.find():
        wr.writerow([str(i['latitude']), str(i['longitude'])])


'''
[list_sorted, points_mapping] = Mapping(step, value)

Discretization (step) all points and save in a .csv
with the name of the equivalent step in meters (value)
If values == none, no save .csv

'''
def Mapping(step, value):

    connection = pm.Connection()
    db = connection["YFCC100M"]

    collection_BCN = db.YFCC100M_BCN

    points = []

    for i in collection_BCN.find():
        point = {"latitude": i['latitude'], "longitude": i['longitude'], "user_id": i["user_id"]}
        points.append(point)

    min_lat = 41.302571
    min_lon = 2.029724
    max_lat = 41.43860847 + step
    max_lon = 2.28858947 + step

    latitudes = []
    longitudes = []

    for i in np.arange(min_lat, max_lat, step):
        latitudes.append(i)
    for i in np.arange(min_lon, max_lon, step):
        longitudes.append(i)

    points_mapping = []
    points_mapping_user = []

    for point in points:
        for latitude in latitudes:
            if math.fabs(float(point["latitude"]) - latitude) <= step/float(2):
                lat = latitude
        for longitude in longitudes:
            if math.fabs(float(point["longitude"]) - longitude) <= step/float(2):
                lon = longitude

        p = [lat, lon]
        points_mapping.append(p)
        pu = [lat, lon, point["user_id"]]
        points_mapping_user.append(pu)

    c = Counter(chain.from_iterable(combinations(x,2) for x in points_mapping))
    c_sorted = c.most_common(len(c))

    if value != None:
        file = open('mapping_'+value+'.csv', 'wb')
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)

        for point in c_sorted:
            wr.writerow([str(point.__getitem__(0).__getitem__(0)), str(point.__getitem__(0).__getitem__(1)), str(point.__getitem__(1))])

    return c_sorted, points_mapping_user

'''
ListPictureInLocation(step, value, lat_pic, lon_pic)

Discretization (step) all points and show the image info
for a given lat_pic and lon_pic (latitude and longitude)
'''

def ListPictureInLocation(step, value, lat_pic, lon_pic):

    connection = pm.Connection()
    db = connection["YFCC100M"]

    collection_BCN = db.YFCC100M_BCN

    points = []

    for i in collection_BCN.find():
        point = {"latitude": i['latitude'], "longitude": i['longitude'], "url_picture": i['download_url'], "user_id": i['user_id'], "tags": i["user_tags"]}
        points.append(point)

    min_lat = 41.302571
    min_lon = 2.029724
    max_lat = 41.43860847 + step
    max_lon = 2.28858947 + step

    latitudes = []
    longitudes = []
    for i in np.arange(min_lat, max_lat, step):
        latitudes.append(i)
    for i in np.arange(min_lon, max_lon, step):
        longitudes.append(i)

    points_mapping = []

    for point in points:
        for latitude in latitudes:
            if math.fabs(float(point["latitude"]) - latitude) <= step/float(2):
                lat = latitude
        for longitude in longitudes:
            if math.fabs(float(point["longitude"]) - longitude) <= step/float(2):
                lon = longitude

        p = [lat, lon, point["url_picture"], point["user_id"], point["tags"]]
        points_mapping.append(p)

    print("Pictures in location: "+"41.3745467"+" - "+"2.1691775")
    for point in points_mapping:

        if ((round(point[0],6) == round(lat_pic,6)) and (round(point[1],6) == round(lon_pic, 6))):
            print "url_pic: "+point[2]
            print "id_user: "+point[3]
            print "tags: "+point[4]


def ListMetadata(lat_pic, lon_pic):

    connection = pm.Connection()
    db = connection["YFCC100M"]

    collection_BCN = db.YFCC100M_BCN

    points = []

    for i in collection_BCN.find():
        point = {"latitude": i['latitude'], "longitude": i['longitude'], "url_picture": i['download_url'], "user_id": i['user_id'], "tags": i["user_tags"]}
        points.append(point)

    min_lat = 41.302571
    min_lon = 2.029724
    max_lat = 41.43860847 + step
    max_lon = 2.28858947 + step

    latitudes = []
    longitudes = []
    for i in np.arange(min_lat, max_lat, step):
        latitudes.append(i)
    for i in np.arange(min_lon, max_lon, step):
        longitudes.append(i)

    points_mapping = []

    for point in points:
        for latitude in latitudes:
            if math.fabs(float(point["latitude"]) - latitude) <= step/float(2):
                lat = latitude
        for longitude in longitudes:
            if math.fabs(float(point["longitude"]) - longitude) <= step/float(2):
                lon = longitude

        p = [lat, lon, point["url_picture"], point["user_id"], point["tags"]]
        points_mapping.append(p)

    print("Pictures in location: "+"41.3745467"+" - "+"2.1691775")
    for point in points_mapping:

        if ((round(point[0],6) == round(lat_pic,6)) and (round(point[1],6) == round(lon_pic, 6))):
            print "url_pic: "+point[2]
            print "id_user: "+point[3]
            print "tags: "+point[4]

