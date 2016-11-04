library(RMongo)
library(ggplot2)
library(ggmap)
library(plotKML)
library(KernSmooth)
library(raster)

# https://en.wikipedia.org/wiki/Multivariate_kernel_density_estimation

db_YFCC100M<-mongoDbConnect('YFCC100M');
query1<-dbGetQuery(db_YFCC100M, 'YFCC100M_BCN',"{}",0,100);

YFCC100M_latitude<-query1['latitude']
YFCC100M_longitude<-query1['longitude']
YFCC100M_user_id<-query1['user_id']
YFCC100M_date_taken<-query1['date_taken']


routes <- data.frame(cbind(query1['user_id'], query1['latitude'], query1['longitude']))
coordinates <- data.frame(cbind(query1['latitude'], query1['longitude']))
barcelona <- qmap(location = 'barcelona', zoom = 12, color = 'bw')

library(ks)
data(coordinates)
H <- Hpi(x=coordinates)
fhat <- kde(x=coordinates, H=H)
plot(fhat, display="filled.contour2")
#points(coordinates, cex=0.5, pch=16)
