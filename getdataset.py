__author__ = 'julian'

import parser
import pymongo

## DATABASE ##

connection = pymongo.Connection()
db = connection["YFCC100M"]

collections_names = db.collection_names()

# ##### Barcelona #####
# for name in collections_names:
#     if name == "YFCC100M_BCN":
#         db.drop_collection("YFCC100M_BCN")
#
# db.create_collection("YFCC100M_BCN")
# collection_BCN = db.YFCC100M_BCN

##### London #####
for name in collections_names:
    if name == "YFCC100M_LND":
        db.drop_collection("YFCC100M_LND")

db.create_collection("YFCC100M_LND")
collection_LND = db.YFCC100M_LND

## PARSER ##

dp = parser.DataParser()
# dp.parse(collection_BCN, "BCN")
dp.parse(collection_LND, "LND")

##### end Barcelona #####



