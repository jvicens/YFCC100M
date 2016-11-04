__author__ = 'julian'


import math
import numpy as np
import pymongo as pm
from datetime import datetime
import pandas as pd
import csv
from collections import Counter
from itertools import chain, combinations
import sklearn as sk
import matplotlib.pyplot as plt


# DBSCAN
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

def databasedata_cluster():
    connection = pm.Connection()
    db = connection["YFCC100M"]

    collection_BCN = db.YFCC100M_BCN

    points_cluster = []

    for i in collection_BCN.find():
        # Access to database information
        point_cluster = {"latitude": i['latitude'], "longitude": i['longitude'],"user_id": i['user_id']}
        points_cluster.append(point_cluster)
    return points_cluster


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
        points_cluster = {"latitude": i['latitude'], "longitude": i['longitude'],"user_id": i['user_id']}
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

#########################
## Spectrum clustering ##
#########################

def spectrum_clustering(points_cluster):
    print(points_cluster)


###########################################################################
## DBSCAN clustering                                                     ##
## http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html ##
###########################################################################

def dbscan(points_cluster):
    # Generate sample data

    data = np.ndarray(shape=(len(points_cluster),2), dtype=float, order='F')
    labels_true = []
    for i, point in enumerate(points_cluster):
        data[i][0] = point['latitude']
        data[i][1] = point['longitude']
        labels_true.append(point['user_id'])

    # Compute DBSCAN
    db = DBSCAN(eps=0.001, min_samples=100).fit(data)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(labels_true, labels))
    print("Adjusted Mutual Information: %0.3f" % metrics.adjusted_mutual_info_score(labels_true, labels))
    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(data, labels))

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)

        xy = data[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)

        xy = data[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.savefig('Cluster_DBSCAN_0.001_100.png')

    #plt.show()

def main():
    #[points, users] = databasedata()
    points_cluster = databasedata_cluster()
    #spectrum_clustering(points_cluster)
    dbscan(points_cluster)
if __name__ == "__main__":
    main()
