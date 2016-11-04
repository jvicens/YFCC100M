library(RMongo)
library(ggplot2)
library(ggmap)
library(plotKML)
library(KernSmooth)
library(raster)
library(fpc)
library(plotrix)

# http://stackoverflow.com/questions/14618657/access-dbscan-cluster-in-r

# Number of samples
N <- 10000
min_points_cluster <- 100
epsilon <- 0.0008

db_YFCC100M<-mongoDbConnect('YFCC100M');
query1<-dbGetQuery(db_YFCC100M, 'YFCC100M_BCN',"{}",0,N);

YFCC100M_latitude<-query1['latitude']
YFCC100M_longitude<-query1['longitude']
YFCC100M_user_id<-query1['user_id']
YFCC100M_date_taken<-query1['date_taken']
YFCC100M_year<-(as.POSIXct(strptime(as.character(YFCC100M_date_taken$date_taken), "%F %H:%M:%OS")))


# routes <- data.frame(cbind(query1['user_id'], query1['latitude'], query1['longitude']))
coordinates <- data.frame(cbind(query1['latitude'], query1['longitude']))
# barcelona <- get_map(location = 'barcelona', zoom = 13, color = 'bw')

# dbscan
ds <- dbscan(coordinates, epsilon, MinPts = min_points_cluster)

# Plot cluster
plot(ds$cluster, main=sprintf("DBSCAN, eps = %s, minPoints = %s.\n All pictures", epsilon, min_points_cluster))
# Plot all clusters
plot(coordinates, col=ds$cluster)
# Plot clusters and hide noise
plot(coordinates[ds$cluster > 0,], col=ds$cluster[ds$cluster>0],main=sprintf("DBSCAN, eps = %s, minPoints = %s.\n All pictures", epsilon, min_points_cluster))

# Cluster adjudicacion
cluster_coordinates = data.frame(cbind(coordinates,ds$cluster))

# Centroid clusters
cluster <- 0
latitude_cluster <- 0
longitude_cluster <- 0
cluster_centroid <- 0
for(i in 1:max(ds$cluster)){
  cluster[i] <- i
  latitude_cluster[i] <- mean(cluster_coordinates[cluster_coordinates$ds.cluster==i,1])
  longitude_cluster[i] <- mean(cluster_coordinates[cluster_coordinates$ds.cluster==i,2])
  
  points(latitude_cluster[i], longitude_cluster[i], pch = 23, bg = "white", col = "white")
  
}
cluster_centroid <- data.frame(cbind(cluster, latitude_cluster, longitude_cluster))

# Path
routes <- data.frame(cbind(query1['user_id'], query1['latitude'], query1['longitude'], ds$cluster))
# http://www.visualcinnamon.com/2014/03/running-paths-in-amsterdam-step-2.html
# Map from Barcelona
barcelona <- qmap(location = 'barcelona', zoom = 13, color = 'bw')
# Map the routes
plot(barcelona + geom_path(aes(x = longitude, y = latitude, group = factor(user_id)), colour="#1E2B6A", data = routes[ds$cluster > 0,], alpha=0.3))
# plot(geom_path(aes(x = longitude, y = latitude, group = factor(user_id)),colour="#1E2B6A", data = routes, alpha=0.3))

##### 
# Delete the pictures taked in the same cluster by the same user
routes_filtered <- routes[!duplicated(routes[,c('user_id', 'ds.cluster')]),]
coordinates_filtered <- data.frame(cbind(routes_filtered['latitude'], routes_filtered['longitude']))
ds_filtered <- dbscan(coordinates_filtered, epsilon, MinPts = min_points_cluster)
# Plot cluster

pdf(file="dbscan_clusters.pdf")
plot(ds_filtered$cluster, xlab="Point", ylab="Cluster")
#axis(side=1, col.ticks="white", col.axis="white") 
#axis(side=2, col.ticks="white", col.axis="white") 
#box("plot", col="white")
dev.off()


# Plot all clusters
plot(coordinates_filtered, col=ds_filtered$cluster, main = "coordinates filtered - noise")
# Plot clusters and hide noise

pdf(file="dbscan_clusters_no_noise.pdf")
plot(coordinates_filtered[ds_filtered$cluster > 0,], col=ds_filtered$cluster[ds_filtered$cluster>0], col.lab="white")
axis(side=1, col.ticks="white", col.axis="white") 
axis(side=2, col.ticks="white", col.axis="white") 
box("plot", col="white")
dev.off()

# Cluster adjudicacion
cluster_coordinates_filtered = data.frame(cbind(coordinates_filtered,ds_filtered$cluster))
# Centroid clusters
cluster_filtered <- 0
latitude_cluster_filtered <- 0
longitude_cluster_filtered <- 0
cluster_filtered_centroid <- 0
for(i in 1:max(ds_filtered$cluster)){
  cluster_filtered[i] <- i
  latitude_cluster_filtered[i] <- mean(cluster_coordinates_filtered[cluster_coordinates_filtered$ds_filtered.cluster==i,1])
  longitude_cluster_filtered[i] <- mean(cluster_coordinates_filtered[cluster_coordinates_filtered$ds_filtered.cluster==i,2])
  points(latitude_cluster_filtered[i], longitude_cluster_filtered[i], pch = 23, bg = "white", col = "white")
  
}
cluster_filtered_centroid <- data.frame(cbind(cluster_filtered, latitude_cluster_filtered, longitude_cluster_filtered))

routes_filtered <- data.frame(cbind(routes_filtered, ds_filtered$cluster))

# Map the routes

pdf(file="path_between_clusters.pdf")
plot(barcelona + geom_path(aes(x = longitude, y = latitude, group = factor(user_id)), colour="#333333", data = routes_filtered[ds_filtered$cluster > 0,], alpha=0.3))
dev.off()

##########################################################################
##########################################################################

spots = read.csv("data/data_spots.csv", header = TRUE)

for (i in 1:max(cluster_coordinates$ds.cluster)){
  
  cluster_ <- cluster_coordinates[cluster_coordinates$ds.cluster==i,c('latitude','longitude')]
  plot(cluster_)
  mean_centerX <- mean(cluster_$latitude)
  mean_centerY <- mean(cluster_$longitude)
  standard_deviationX <- sd(cluster_$latitude)
  standard_deviationY <- sd(cluster_$longitude)
  standard_distance <- sqrt(sum(((cluster_$latitude-mean_centerX)^2+(cluster_$longitude-mean_centerY)^2))/(nrow(cluster_)))
  print(standard_distance)
  distances <- matrix(, nrow = length(spots$spot), ncol =  1)
  
  
  max_centerX <- max((cluster_$latitude-mean_centerX)^2)
  max_centerY <- max((cluster_$longitude-mean_centerY)^2)
  max_standard_distance <- sqrt(max_centerY+max_centerX)/2
  
  for (i in 1:length(spots$spot)) {
    distances[i,] <- sqrt((spots$lat[i]-mean_centerX)^2+(spots$lon[i]-mean_centerY)^2)/2
    #distances[i,] <- i
  }
  cols <- c("blue", "red")[(distances == min(distances)) + 1]
  a <- c("n",spots$spot)[(distances == min(distances))]
  b <- barplot(distances[,1], col = cols, names.arg = spots$spot, cex.names = 0.5,cex.lab= 0.1, las=2)
  abline(standard_distance,0, col = 'red')

  
  #jpeg("PP_Circle.jpeg",2500,2000,res=300)
  plot(cluster_,pch="+",cex=0.5,main="")
  points(mean_centerX,mean_centerY,col="red",pch=16)
  draw.circle(mean_centerX,mean_centerY,radius=standard_distance,border="red",lwd=1)
  draw.circle(mean_centerX,mean_centerY,radius=max_standard_distance,border="red",lwd=2)
  #dev.off()
}



