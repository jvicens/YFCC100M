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
YFCC100M_user_tags<-query1['user_tags']

YFCC100M_year<-(as.POSIXct(strptime(as.character(YFCC100M_date_taken$date_taken), "%F %H:%M:%OS")))


for (i in length(YFCC100M_user_tags) ) {
  print(YFCC100M_user_tags[i])
  print(strsplit((YFCC100M_user_tags[i]), "[,]"))
}

# routes <- data.frame(cbind(query1['user_id'], query1['latitude'], query1['longitude']))
coordinates <- data.frame(cbind(query1['latitude'], query1['longitude']))
# barcelona <- get_map(location = 'barcelona', zoom = 13, color = 'bw')

