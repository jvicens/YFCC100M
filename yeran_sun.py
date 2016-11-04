__author__ = 'julian'


import math
import numpy as np
import pymongo as pm
from datetime import datetime
import pandas as pd
import csv
from collections import Counter
from itertools import chain, combinations


def databasedata():
    connection = pm.Connection()
    db = connection["YFCC100M"]

    collection_BCN = db.YFCC100M_BCN

    points = []

    users = []
    user_metadata = []

    for i in collection_BCN.find():
        # Access to database information
        point = {"date_taken": i['date_taken'], "latitude": i['latitude'], "longitude": i['longitude'], "url_picture": i['download_url'], "user_id": i['user_id'], "tags": i["user_tags"].split(',')}
        # Data from 01/01/2010
        if i['date_taken'] is not None and not i['date_taken'] == "null":
            if datetime.strptime(i['date_taken'], '%Y-%m-%d %H:%M:%S.%f') > datetime(2010, 01, 01):
                points.append(point)

                # Metadata information by user
                # yearmonth: count by user
                user_metadata = {
                    "date_taken": i['date_taken'],
                    "latitude": i['latitude'],
                    "longitude": i['longitude'],
                    "url_picture": i['download_url'],
                    "tags": i["user_tags"].split(','),
                }

        user_saved = False

        # Group by users
        for user in users:
            if user['user_id'] == i['user_id']:
                # Data from 01/01/2010
                if datetime.strptime(i['date_taken'], '%Y-%m-%d %H:%M:%S.%f') > datetime(2010, 01, 01):
                    user['metadata'].append(user_metadata)

                user_saved = True
                break

        if not user_saved:
            user = {
                'user_id': i['user_id'],
                'metadata': [user_metadata],
                "entropy_pictures_date": 0,

            }
            # Data from 01/01/2010
            if i['date_taken'] is not None and not i['date_taken'] == "null":
                if datetime.strptime(i['date_taken'], '%Y-%m-%d %H:%M:%S.%f') > datetime(2010, 01, 01):
                    users.append(user)

    print 'total_points: '+str(len(points))
    print 'total_users: '+str(len(users))
    return [points, users]

#################################################
## Division users between residents and locals ##
#################################################

def residents_vs_tourist(users):
    for user in users:
        pictures_date = []
        for metadata in user['metadata']:
            pictures_date.append(int(metadata['date_taken'].split('-')[0]+metadata['date_taken'].split('-')[1]))

        picture_date_series = pd.Series(pictures_date)
        picture_date_counts_series = picture_date_series.value_counts()
        sum_pictures_di = sum(picture_date_counts_series)
        e = 0
        for pictures_month in picture_date_counts_series:
            pi = float(pictures_month)/float(sum_pictures_di)
            e = e - (pi * math.log(pi, 10))

        #if (e > 0.5):
        #    print(user)
        #    raw_input("Press Enter to continue...")
        user['entropy_pictures_date'] = e
        #print e


def main():
    [points, users] = databasedata()
    #residents_vs_tourist(users)

if __name__ == "__main__":
    main()

