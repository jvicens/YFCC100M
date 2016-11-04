library(RMongo)
library(ggplot2)
library(ggmap)
library(plotKML)
library(KernSmooth)
library(raster)
library(fpc)
library(lattice)

# http://stackoverflow.com/questions/14618657/access-dbscan-cluster-in-r

# Number of samples
N <- 10000
# Number of points
points <- seq(100,500,100)
# Epsilon
epsilons <- seq(0.0001,0.0006,0.0001)

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

m_number_of_clusters = matrix(, nrow = length(points), ncol =  length(epsilons), dimnames = list(points, epsilons))
m_points_no_clustered = matrix(, nrow = length(points), ncol = length(epsilons), dimnames = list(points, epsilons))

i_points <- 1
for (n_points in points){
  i_epsilon <- 1
  print(sprintf("Points = %s", n_points))
  for(epsilon in epsilons){
    ds <- dbscan(coordinates, epsilon, MinPts = n_points)
    m_number_of_clusters[i_points,i_epsilon] <- max(ds$cluster)
    m_points_no_clustered[i_points,i_epsilon] <- length(ds$cluster[ds$cluster==0])
    setEPS()
    if(max(ds$cluster)>0){
      postscript(sprintf("dbscan_heatmaps/DBSCAN_%s_%s_%s_all.eps", epsilon, n_points, N))
      plot(coordinates[ds$cluster > 0,], col=ds$cluster[ds$cluster>0])
      dev.off()
    }

    
    # Find centroide clusters
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
    }
    cluster_centroid <- data.frame(cbind(cluster, latitude_cluster, longitude_cluster))
    write.csv(cluster_centroid, file = sprintf("dbscan_heatmaps/cluster_centroid_%s_%s_%s_all.csv", epsilon, n_points, N),  na="")
    
    # print(cluster_centroid)
    # cat ("Press [enter] to continue")
    # line <- readline()
    ##
    i_epsilon <- i_epsilon + 1
    print(sprintf("Epsilon = %s", epsilon))
    print(max(ds$cluster))
  }
  i_points <- i_points + 1
}
levelplot(m_number_of_clusters, Rowv=NA, Colv=NA, xlab="number of points", ylab="epsilon", col.regions = gray(0:100/100))
write.csv(m_number_of_clusters, file = "dbscan_heatmaps/number_of_clusters.csv",  na="")
postscript(sprintf("dbscan_heatmaps/number_of_clusters.eps"))
levelplot(m_number_of_clusters, Rowv=NA, Colv=NA, xlab="number of points", ylab="epsilon", col.regions = gray(0:100/100))
dev.off()

levelplot(m_points_no_clustered, Rowv=NA, Colv=NA, xlab="number of points", ylab="epsilon", col.regions = gray(0:100/100))
write.csv(m_points_no_clustered, file = "dbscan_heatmaps/points_no_clustered.csv", na="")
postscript(sprintf("dbscan_heatmaps/points_no_clustered.eps"))
levelplot(m_points_no_clustered, Rowv=NA, Colv=NA, xlab="number of points", ylab="epsilon", col.regions = gray(0:100/100))
dev.off()

##########################################################################
##########################################################################



