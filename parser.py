__author__ = 'julian'

"""
* Photo/video identifier
* User NSID
* User nickname
* Date taken
* Date uploaded
* Capture device
* Title
* Description
* User tags (comma-separated)
* Machine tags (comma-separated)
* Longitude
* Latitude
* Accuracy
* Photo/video page URL
* Photo/video download URL
* License name
* License URL
* Photo/video server identifier
* Photo/video farm identifier
* Photo/video secret
* Photo/video secret original
* Extension of the original photo
* Photos/video marker (0 = photo, 1 = video)

"""


import bz2
from io import BytesIO

import numpy as np
from PIL import Image
import requests

# keys for the YFCC100M data
YFCC100M_KEYS = [
    "photo_id",
    "user_id",
    "username",
    "date_taken",
    "upload_time",
    "camera_type",
    "title",
    "description",
    "user_tags",
    "machine_tags",
    "longitude",
    "latitude",
    "accuracy",
    "page_url",
    "download_url",
    "license",
    "license_url",
    "server",
    "farm",
    "secret",
    "original",
    "extension",
    "image_or_video"
]

def image_from_url(url):
    """
        Downloads an image in numpy array format, given a URL.
    """

    # loop until the image is successfully downloaded
    status = None
    while status != 200:
        response = requests.get(url)
        status = response.status_code
    pimg = Image.open(BytesIO(response.content))
    pimg = pimg.convert("RGB")

    # convert to numpy array and return
    return np.asarray(pimg)


class DataParser():

    def __init__(self):

        return None

    def parse(self, collection, place):

        for index_set in range(0, 10):
            print("dataset/yfcc100m_dataset-"+str(index_set)+".bz2")

            with bz2.BZ2File("dataset/yfcc100m_dataset-"+str(index_set)+".bz2", "r") as file:
                for line in file:
                    # fit the data into a dictionary
                    values = [item.strip() for item in line.split("\t")]
                    data = dict(zip(YFCC100M_KEYS, values))
                    data["camera_type"] = data["camera_type"].lower()

                    # BARCELONA AREA
                    if place == "BCN":
                        if ((data["latitude"] != '') & (data["longitude"] != '')) and (
                            ((float(data["latitude"]) > 41.302571) & (float(data["longitude"]) > 2.029724)) & (
                            (float(data["latitude"]) < 41.43860847) & (float(data["longitude"]) < 2.28858947))):
                        # check image or video
                        # if data["image_or_video"] == "0":
                        # download the image
                        # data["image"] = image_from_url(data["download_url"])
                            collection.insert(data)

                    # LONDON AREA
                    if place == "LND":
                        if ((data["latitude"] != '') & (data["longitude"] != '')) and (
                            ((float(data["latitude"]) > 51.255809) & (float(data["longitude"]) > -0.606996)) & (
                            (float(data["latitude"]) < 51.734595) & (float(data["longitude"]) < 0.348814))):
                        # check image or video
                        # if data["image_or_video"] == "0":
                        # download the image
                        # data["image"] = image_from_url(data["download_url"])
                            collection.insert(data)

            print "total:" +str(collection.count())

