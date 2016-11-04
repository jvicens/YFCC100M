__author__ = 'julian'

import pymongo as pm
import numpy as np
import csv
import math
import time, datetime
from collections import Counter
from itertools import chain, combinations
import matplotlib
import pylab as plt


'''
# Solve the issue about rare characters in the database

import urllib
urllib.unquote(line)

'''
## DATABASE ##
'''
users()

User's list sorted by repeated number of pictures
'''
def users_pictures():

    connection = pm.Connection()
    db = connection["YFCC100M"]

    collection_BCN = db.YFCC100M_BCN

    points = []
    users = []

    for i in collection_BCN.find():
        point = {"user": i['user_id'], "latitude": i['latitude'], "longitude": i['longitude'], "timestamp": i['date_taken']}
        points.append(point)
        users.append(i['user_id'])

    c = Counter(users)
    c_sorted = c.most_common(100)

    points_user = []

    for point in points:
        if point['user'] == c_sorted[0][0]:
            points_user.append(point)

    print(points_user)

'''
users_spot()

Given an discretizated spot distribution of users picture in
each spot
'''

def users_spot(list_sorted, points_mapping):

    users_spots = []

    for spot in list_sorted:

        spot_lat = spot[0][0]
        spot_lon = spot[0][1]
        users_list = []

        for point in points_mapping:
            if ((round(point[0],6) == round(spot_lat,6)) and (round(point[1],6) == round(spot_lon, 6))):
                users_list.append(point[2])

        c = Counter(users_list) #number of pictures per user
        c.most_common(len(c))

        #print(c)

        user_per_spot = [spot_lat, spot_lon, len(c)]
        users_spots.append(user_per_spot)

    file = open('users_per_spot.csv', 'wb')
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)

    for us in users_spots:
        wr.writerow([str(us[0]), str(us[1]), str(us[2])])


'''
1. Discretization coordinates
2. Unique users in each spot

'''

def users_per_spot(step, value):

    connection = pm.Connection()
    db = connection["YFCC100M"]

    collection_BCN = db.YFCC100M_BCN

    points = []

    for i in collection_BCN.find():
        point = {"latitude": i['latitude'],
                 "longitude": i['longitude'],
                 "url_picture": i['download_url'],
                 "user_id": i['user_id'],
                 "tags": i["user_tags"]}

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

    print "> discretization map"

    points_mapping = []
    points_mapping_info = []

    for point in points:
        for latitude in latitudes:
            if math.fabs(round(float(point["latitude"]), 6) - round(latitude, 6)) <= step/float(2):
                lat = latitude
        for longitude in longitudes:
            if math.fabs(round(float(point["longitude"]), 6) - round(longitude, 6)) <= step/float(2):
                lon = longitude

        p = [lat, lon]
        points_mapping.append(p) ### points_mapping : discretization coordinates

        pinfo = [lat, lon, point["url_picture"], point["user_id"], point["tags"]]
        points_mapping_info.append(pinfo)

    c = Counter(chain.from_iterable(combinations(x,2) for x in points_mapping))

    c_sorted = c.most_common(len(c)) ### c_sorted : coordinates sorted by accumulated

    print "> sorted accumulate pictures"

    users_spots = []

    for spot in c_sorted:

        spot_lat = spot[0][0]
        spot_lon = spot[0][1]
        users_list = []

        for point in points_mapping_info:
            if ((round(point[0],6) == round(spot_lat, 6)) and (round(point[1],6) == round(spot_lon, 6))):
                users_list.append(point[3]) ### users_list : user list in each spot

        c = Counter(users_list) ### c : number of pictures per each user
                                ### user and number of user's pictures
        #c_sorted = c.most_common(len(c)) ### sorted user most to low number of pictures



        ### user_per_spot : lat, lon, total different users and c
        user_per_spot = [spot_lat, spot_lon, len(c), c]
        #print(len(c))

        users_spots.append(user_per_spot) ### list per each spot

    print "> user's spots"

    file = open('users_per_spot_'+value+'.csv', 'wb')
    file2 = open('mapping_users_spot_'+value+'.csv', 'wb')
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    wr2 = csv.writer(file2, quoting=csv.QUOTE_ALL)
    wr.writerow(["latitude", "longitude", "id_user", "pictures_user"])
    wr2.writerow(["latitude", "longitude", "total_user_spot"])
    for us in users_spots:
        wr2.writerow([us[0], us[1], us[2]])
        for i in range(0,us[2]):
            wr.writerow([us[0], us[1], us[3].keys()[i], us[3].values()[i]])

    print "csv with user data"

#####################################################################################################
#
# 1. Total users
#   [id, lat, lon, acc, timestamp] -> users_bcn.csv
# 2. Pictures accumulate per each user
#   [id, total_pictures] -> users_bcn_acc.csv
# Discretization space (100m - 0.0008997 GSP) and time (1h - 3600s).
# 3. Total users [id, lat, lon, acc, mean_error, timestamp, mean_error] -> users_bcn_disc.csv
# 4. Pictures accumulate per each user -> users_bcn_acc_disc.csv
#
######################################################################################################

def Users():

    #users_total()
    #user_discretization_position(0.0008997, "100m")
    #user_discretization_time(3600, "1h")
    #user_discretization_space_and_time(0.0008997, 3600, "100m", "1h")
    user_data()

def user_data():
    list_users = []
    with open('users_bcn_discrete_position_and_time_100m_1h.csv', 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in data:
            user_info = {
                "user_id":row[0],
                "latitude": row[1],
                "latitude_": row[2],
                "error_latitude_": row[3],
                "longitude": row[4],
                "longitude_": row[5],
                "error_longitude_": row[6],
                "accuracy": row[7],
                "date": row[8],
                "date_": row[9],
                "timestamp": row[10],
                "timestamp_": row[11],
                "error_timestamp_": row[12]
            }

            user_found = False
            for u in list_users:
                if u['id'] == user_info['user_id']:
                    list_data = u['data']
                    list_data.append(user_info)
                    u['data'] = list_data
                    user_found = True
            if not user_found:
                list_data = []
                list_data.append(user_info)
                user = {
                    "id": row[0],
                    "data":list_data
                }
                list_users.append(user)

        print '>> User spots'
        i = 1
        ids_users = []
        ids_label = []
        total_pictures = []

        for user in list_users:
            if (len(user['data']) > 100):
                ids_label.append(i)
                i += 1
                ids_users.append(user['id'])
                total_pictures.append(len(user['data']))
                print 'id'+str(user['id'])+' - '+'total: '+str(len(user['data']))

        return list_users



def user_discretization_space_and_time(step, interval, str_distance, str_interval):

    connection = pm.Connection()
    db = connection["YFCC100M"]

    collection_BCN = db.YFCC100M_BCN

    points = []

    for i in collection_BCN.find():
        point = {
            "user_id": i['user_id'],
            "latitude": i['latitude'],
            "latitude_": "",
            "error_latitude_": "",
            "longitude": i['longitude'],
            "longitude_": "",
            "error_longitude_": "",
            "accuracy": i['accuracy'],
            "date": i['date_taken'],
            "date_": "",
            "timestamp": "",
            "timestamp_": "",
            "error_timestamp_": ""
        }

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
    points_mapping_info = []

    file = open('users_bcn_discrete_position_and_time_'+str_distance+'_'+str_interval+'.csv', 'wb')
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    wr.writerow(["user_id",
                 "latitude", "latitude_", "error_latitude_",
                 "longitude", "longitude_", "error_longitude_",
                 "accuracy",
                 "date", "date_",
                 "timestamp", "timestamp_", "error_timestamp_"])

    for point in points:
        for latitude in latitudes:
            if math.fabs(round(float(point["latitude"]), 6) - round(latitude, 6)) <= step/float(2):
                point['latitude_'] = round(latitude, 6)
                point['error_latitude_'] = round(float(point["latitude"]), 6) - round(latitude, 6)

        for longitude in longitudes:
            if math.fabs(round(float(point["longitude"]), 6) - round(longitude, 6)) <= step/float(2):
                point['longitude_'] = round(longitude, 6)
                point['error_longitude_'] = round(float(point["longitude"]), 6) - round(longitude, 6)

        if point['date'] and not point['date'] == 'null':

            dt = datetime.datetime.strptime(point['date'], "%Y-%m-%d %H:%M:%S.%f")
            if dt.year >= 1970:
                t = time.mktime(datetime.datetime.strptime(point['date'], "%Y-%m-%d %H:%M:%S.%f").timetuple())

                point['timestamp'] = t
                pt = t - (t % interval)
                point['timestamp_'] = pt
                point['date_'] = datetime.datetime.fromtimestamp(pt).strftime('%Y-%m-%d %H:%M:%S')
                point['error_timestamp_'] = t-pt

            else:
                print 'error year: '+str(dt.year)
        else:
            print 'date null'

        wr.writerow([point['user_id'],
                     point['latitude'], point['latitude_'], point['error_latitude_'],
                     point['longitude'], point['longitude_'], point['error_longitude_'],
                     point['accuracy'],
                     point['date'], point['date_'],
                     point['timestamp'], point['timestamp_'], point['error_timestamp_']])

    file.close()
    print('> end discretization')


def user_discretization_time(interval, string_interval):
    connection = pm.Connection()
    db = connection["YFCC100M"]

    collection_BCN = db.YFCC100M_BCN

    points = []

    file = open('users_bcn_discrete_time_'+string_interval+'.csv', 'wb')
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    wr.writerow(["user_id", "latitude", "longitude", "accuracy", "date", "date_", "timestamp",
                 "timestamp_", "error_timestamp_"])

    for i in collection_BCN.find():
        point = {
            "user_id": i['user_id'],
            "latitude": i['latitude'],
            "longitude": i['longitude'],
            "accuracy": i['accuracy'],
            "date": i['date_taken'],
            "date_": "",
            "timestamp": "",
            "timestamp_": "",
            "error_timestamp_": ""
        }
        if point['date'] and not point['date'] == 'null':

            dt = datetime.datetime.strptime(point['date'], "%Y-%m-%d %H:%M:%S.%f")
            if dt.year >= 1970:
                t = time.mktime(datetime.datetime.strptime(point['date'], "%Y-%m-%d %H:%M:%S.%f").timetuple())

                point['timestamp'] = t
                pt = t - (t % interval)
                point['timestamp_'] = pt
                point['date_'] = datetime.datetime.fromtimestamp(pt).strftime('%Y-%m-%d %H:%M:%S')
                point['error_timestamp_'] = t-pt

                wr.writerow([point['user_id'], point['latitude'], point['longitude'], point['accuracy'], point['date'],
                     point['date_'], point['timestamp'], point['timestamp_'], point['error_timestamp_']])

            else:
                print 'error year: '+str(dt.year)
        else:
            print 'date null'

    file.close()



def user_discretization_position(step, distance):

    connection = pm.Connection()
    db = connection["YFCC100M"]

    collection_BCN = db.YFCC100M_BCN

    points = []

    for i in collection_BCN.find():
        point = {
            "user_id": i['user_id'],
            "latitude": i['latitude'],
            "longitude": i['longitude'],
            "accuracy": i['accuracy'],
            "timestamp": i['date_taken'],
            "latitude_": "",
            "longitude_": "",
            "error_latitude_": "",
            "error_longitude_": ""
        }

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
    points_mapping_info = []

    file = open('users_bcn_discrete_position_'+distance+'.csv', 'wb')
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    wr.writerow(["user_id", "latitude", "longitude", "accuracy", "timestamp", "latitude_", "longitude_",
                 "error_latitude_", "error_longitude_"])

    print('> discretization position '+distance)

    for point in points:
        for latitude in latitudes:
            if math.fabs(round(float(point["latitude"]), 6) - round(latitude, 6)) <= step/float(2):
                point['latitude_'] = round(latitude, 6)
                point['error_latitude_'] = round(float(point["latitude"]), 6) - round(latitude, 6)

        for longitude in longitudes:
            if math.fabs(round(float(point["longitude"]), 6) - round(longitude, 6)) <= step/float(2):
                point['longitude_'] = round(longitude, 6)
                point['error_longitude_'] = round(float(point["longitude"]), 6) - round(longitude, 6)

        wr.writerow([point['user_id'], point['latitude'], point['longitude'], point['accuracy'], point['timestamp'],
                     point['latitude_'], point['longitude_'], point['error_latitude_'], point['error_longitude_']])

    file.close()
    print('> end discretization')

def users_total():
    #### Total users
    connection = pm.Connection()
    db = connection["YFCC100M"]

    collection_BCN = db.YFCC100M_BCN

    points = []
    users = []

    for i in collection_BCN.find():
        point = {
            "user_id": i['user_id'],
            "latitude": i['latitude'],
            "longitude": i['longitude'],
            "accuracy": i['accuracy'],
            "timestamp": i['date_taken']
        }
        points.append(point)
        users.append(i['user_id'])

    print('> points')
    print(' > total points: %d' % len(points))

    c_users = Counter(users)
    print('> users')
    print(' > total points: %d' % len(c_users))
    c_users_sorted = c_users.most_common(len(c_users))

    ### create csv
    print('> creating users_bcn.csv')

    file = open('users_bcn.csv', 'wb')
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    wr.writerow(["user_id", "latitude", "longitude", "accuracy", "timestamp"])
    for point in points:
        wr.writerow([point['user_id'], point['latitude'], point['longitude'], point['accuracy'], point['timestamp']])

    file.close()

    print('> created users_bcn.csv')
    print('> creating users_bcn_acc.csv')

    file = open('users_bcn_acc.csv', 'wb')
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    wr.writerow(["user_id", "total_pictures"])
    for user in c_users_sorted:
        wr.writerow([user[0], user[1]])

    file.close()
    print('> created users_bcn_acc.csv')
