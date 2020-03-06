import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import seaborn as sns
from pyproj import Proj, transform
import folium
from folium.plugins import HeatMap
import geopandas as gpd
import pyarrow

import random
from tqdm import tqdm, trange

import math
import pprint as pp
from datetime import datetime

from itertools import product
from string import ascii_uppercase
from matplotlib import patheffects

def timetest(time_range):
    data_df = pd.DataFrame(columns=['time', 'lat', 'long', 'ratio'])
    highest = 0
    # just downtown core
    # lng_range = 49538.762
    # lat_range = 37701.149
    lng_max = 572548.325  # State line meters 0405
    lng_min = 523009.563 + (86 * 500) - 1000  # State line meters 0405
    lng_max = lng_min + 2000
    lat_max = 1986392.399  # State line meters 0405
    lat_min = 1948691.250 + (41 * 500) - 1000  # State line meters 0405
    lat_max = lat_min + 2000
    grid_increment = 5
    # lat_min = 1948691.250 # State line meters 0405
    # lat_max = 1948691.250 # State line meters 0405
    lng_range = lng_max - lng_min
    lat_range = lat_max - lat_min
    lng_loops = math.ceil(lng_range / grid_increment)
    lat_loops = math.ceil(lat_range / grid_increment)
    # parquetdataname = "C:/ticketdodger/python/data/test/testdata.parquet"
    # data_df = pd.read_parquet(parquetdataname)
    for t in trange(time_range, desc="time loop"):

        time = (t / 23)
        # outProj = Proj("esri:102645", preserve_units=False)
        # inProj = Proj("epsg:4326") # WGS84 in lat long
        # # y1, x1 = (560301.731, 1976879.710) # Center LA
        # y1, x1 = (34.0434, -118.2504)
        # x2, y2 = transform(inProj, outProj, y1, x1)

        starttime = (str(t) + "00").zfill(4)
        endtime = starttime[:2] + "59"
        parquetname = "../data/tickets_" + starttime + "_to_" + endtime + ".parquet"
        df = pd.read_parquet(parquetname)
        # Full data range
        # lng_range = 115529.80704000004
        # lat_range = 114956.93543999991
        # lng_max = 638458.22016  # State line meters 0405
        # lng_min = 522928.41312  # State line meters 0405
        # lat_max = 2027717.99688  # State line meters 0405
        # lat_min = 1912761.06144  # State line meters 0405


        for y in trange(lat_loops, desc="lat loop"):
            print('starting lat square' + str(y))
            for z in trange(lng_loops, desc="lng loop"):
                x2 = 500 + (y * grid_increment) + lat_min
                y2 = 500 + (z * grid_increment) + lng_min
                areatotal = len(df[(df.Latitude >= (x2 - 500)) & (df.Latitude <= (x2 + 500)) & (
                            df.Longitude >= (y2 - 500)) & (df.Longitude <= (y2 + 500))].index)
                if highest < areatotal:
                    highest = areatotal
                    print("new highest = " + str(highest) + " at lat square: " + str(y) + " and lng square: " + str(z) + " and grid increment size = " + str(grid_increment))
                    location = "highest = " + str(highest) + " at lat square: " + str(y) + " and lng square: " + str(z) + " and grid increment size = " + str(grid_increment)


    return location


print(timetest(1))
# 1129