__author__ = 'julian'

"""
==========================================================================
http://geoffboeing.com/2014/08/clustering-to-reduce-spatial-data-set-size/
==========================================================================
"""
# magic command to display matplotlib plots inline within the ipython notebook webpage

# import necessary modules
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from time import time
from sklearn.cluster import DBSCAN
from sklearn import metrics
from geopy.distance import great_circle

def plotClusters():
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    # for each label (aka index) in the set of unique labels
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        # boolean array as a mask for all labels that match the current one in the loop
        class_member_mask = (labels == k)

        # the xy point pairs from the original data set that match this cluster
        xy = coordinates[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)

        # and the inverse
        xy = coordinates[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % num_clusters)
    plt.show()

# return the coordinates of the centroid of a numpy array of coordinate points
def getCentroid(points):
    n = points.shape[0]
    sum_lon = np.sum(points[:, 1])
    sum_lat = np.sum(points[:, 0])
    return (sum_lon/n, sum_lat/n)

# return the point from a set of points that is nearest to the specified point of reference
def getNearestPoint(set_of_points, point_of_reference):

    closest_point = None
    closest_dist = None

    for point in set_of_points:

        # calculate the great circle distance between points
        point = (point[1], point[0])
        dist = great_circle(point_of_reference, point).meters

        # if this row's nearest is currently null, save this point as its nearest
        # or if this distance is smaller than the previous smallest, update the row
        if (closest_dist is None) or (dist < closest_dist):
            closest_point = point
            closest_dist = dist

    return closest_point


# return the rows from full_set that have matching 'lat' 'lon' coordinates in the simplified_set
def getMatchingRows(full_set, simplified_set):

    start_time = time()
    simplified_set['fs_index'] = None

    # fs_index will contain the index of the matching row from the full set
    simplified_set['fs_index'] = None

    # for each coordinate pair in the simplified set
    for si_i, si_row in simplified_set.iterrows():

        si_coords = (si_row['lat'], si_row['lon'])
        # for each coordinate pair in the original full data set
        for fs_i, fs_row in full_set.iterrows():

            # compare tuples of coordinates, if the points match, save this row's index as the matching one
            if si_coords == (fs_row['lat'], fs_row['lon']):
                simplified_set.loc[si_i, 'fs_index'] = fs_i
                break

    # select the rows from the original full data set whose indices appear in fs_index column of the simplified set
    result = full_set.ix[simplified_set['fs_index'].dropna()]
    print 'process took %s seconds' % round(time() - start_time, 2)
    return result

# load the data set
df = pd.read_csv('users_bcn.csv')
coordinates = df.as_matrix(columns=['longitude', 'latitude'])
df.head()

# Compute DBSCAN
# eps is the physical distance from each point that forms its epsilon-neighborhood
# min_samples is the min cluster size, otherwise it's noise - set to 1 so we get no noise
start_time = time()
db = DBSCAN(eps=.01, min_samples=1).fit(coordinates)
labels = db.labels_

# number of clusters in labels, ignoring noise if present
num_clusters = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % num_clusters)
#print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(coordinates, labels))
print 'process took %s seconds' % round(time() - start_time, 2)

plotClusters()

# now we take one point's coordinates from each cluster that formed
# first, get the clusters
start_time = time()
clusters = pd.Series([coordinates[labels == i] for i in xrange(num_clusters)])

lat = []
lon = []

# for each cluster, find one representative point from the data set
for i, cluster in clusters.iteritems():

    if len(cluster) < 3:
        # if there are only one or two points in the cluster,
        # then just take the first coordinate pair that appears in the cluster's array
        representative_point = (cluster[0][1], cluster[0][0])

    else:
        # otherwise, find the point in the cluster that is closest to its centroid
        representative_point = getNearestPoint(cluster, getCentroid(cluster))

    lat.append(representative_point[0])
    lon.append(representative_point[1])

cl = pd.DataFrame({'lon':lon, 'lat':lat})
print 'process took %s seconds' % round(time() - start_time, 2)
print len(cl), 'rows in the reduced data set'
cl.head()

rs = getMatchingRows(df, cl)

rs.sort(inplace=True)
#rs.to_csv('data/summer-travel-gps-dbscan.csv', index=False)

print 'number of points:', len(rs.index)
rs.tail()

# plot the final reduced set of coordinate points vs the original full set
plt.figure(figsize=(10, 6), dpi=100)
rs_scatter = plt.scatter(rs['lon'], rs['lat'], c='g', alpha=.4, s=150)
df_scatter = plt.scatter(df['lon'], df['lat'], c='k', alpha=.5, s=5)

plt.title('Full data set vs DBSCAN reduced set')
plt.legend((df_scatter, rs_scatter), ('Full set', 'Reduced set'), loc='upper left')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.show()
