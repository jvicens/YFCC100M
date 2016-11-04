library(RMongo)
library(ggplot2)
library(ggmap)
library(plotKML)

db_YFCC100M<-mongoDbConnect('YFCC100M');
query1<-dbGetQuery(db_YFCC100M, 'YFCC100M_BCN',"{}",0,1000);

YFCC100M_latitude<-query1['latitude']
YFCC100M_longitude<-query1['longitude']
YFCC100M_user_id<-query1['user_id']
YFCC100M_date_taken<-query1['date_taken']


routes <- data.frame(cbind(query1['user_id'], query1['latitude'], query1['longitude']))


# http://www.visualcinnamon.com/2014/03/running-paths-in-amsterdam-step-2.html
# Map from Barcelona
barcelona <- qmap(location = 'barcelona', zoom = 12, color = 'bw')
# Map the routes
plot(barcelona + geom_path(aes(x = longitude, y = latitude, group = factor(user_id)), 
            colour="#1E2B6A", data = routes, alpha=0.3))


