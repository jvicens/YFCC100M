__author__ = 'julian'

import mapping
import visualization
import filter
import pylab as plt


####### Mapping #######

# step = 0.00008997 #10m
# step = 0.0008997 #100m
# step = 0.008997 #1000m

# mapping.Mapping(0.008997, "1000m")
# mapping.Mapping(0.0008997, "100m")
# mapping.Mapping(0.00008997, "10m")

# mapping.ListPictureInLocation(0.0008997, "", 41.374547, 2.169178)

# mapping.MappingAll()

#######

####### Visualization #######

# visualization.scatter_plot("mapping_bcn/mapping_1000m.csv", "1000m")

#######

####### Analysis #######

# analysis.users()


## List spots most visited

# [list_sorted, points_mapping] = mapping.Mapping(0.0008997, None)
# analysis.users_spot(list_sorted, points_mapping)


# filter.users_per_spot(0.00008997, "10m")

# print(list_sorted[0][0][0]) #latitude
# print(list_sorted[0][0][1]) #longitude
# print(list_sorted[0][1]) #total


## Distribution per users of the spot

#######

####### Filter Users ########

list_users = filter.Users();

print(list_users_sorted)


