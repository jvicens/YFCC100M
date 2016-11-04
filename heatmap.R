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
barcelona <- get_map(location = 'barcelona', zoom = 13, color = 'bw')

# Draw the heat map
ggmap(barcelona, extent = "device") + 
  geom_density2d(data = coordinates, aes(x = longitude, y = latitude), size = 0.03) + 
  stat_density2d(data = coordinates, 
                 n = 1000, 
                 aes(x = longitude, 
                     y = latitude, 
                     fill = ..level.., 
                     alpha = ..level..), 
                 size = 0.1, 
                 geom = "polygon") + 
  scale_fill_gradient(low = "white", high = "#1E2B6A") + 
  scale_alpha(range = c(0, 0.3), guide = FALSE)