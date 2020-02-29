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
from datetime import datetime

from itertools import product
from string import ascii_uppercase
from matplotlib import patheffects

# import tracemalloc
#
# tracemalloc.start()


def timetest(time_range, r):
    data_df = pd.DataFrame(columns=['time', 'lat', 'long', 'ratio'])
    # parquetdataname = "C:/ticketdodger/python/data/test/testdata.parquet"
    # data_df = pd.read_parquet(parquetdataname)
    dictionarylist = []
    for t in trange(time_range, desc="time loop"):

        time = (t / 23)
        # outProj = Proj("esri:102645", preserve_units=False)
        # inProj = Proj("epsg:4326") # WGS84 in lat long
        # # y1, x1 = (560301.731, 1976879.710) # Center LA
        # y1, x1 = (34.0434, -118.2504)
        # x2, y2 = transform(inProj, outProj, y1, x1)

        starttime = (str(t) + "00").zfill(4)
        endtime = starttime[:2] + "59"
        parquetname = "C:/ticketdodger/python/data/tickets_" + starttime + "_to_" + endtime + ".parquet"
        df = pd.read_parquet(parquetname)

        lng_range = 115529.80704000004
        lat_range = 114956.93543999991
        lng_max = 638458.22016  # State line meters 0405
        lng_min = 522928.41312  # State line meters 0405
        lat_max = 2027717.99688  # State line meters 0405
        lat_min = 1912761.06144  # State line meters 0405

        for y in trange(r, desc="count loop"):
            #ddf = df
            # print("starting rep: " + str(y))
            random_x = random.random()
            random_y = random.random()
            x2 = (random_x * lat_range) + lat_min

            # print("random lat: " + str(x2))
            y2 = (random_y * lng_range) + lng_min
            # print("random long: " + str(y2))
            timetotal = len(df.index)
            # print("len of df: " + str(timetotal))
            areatotal = len(df[(df.Latitude >= (x2 - 1000)) & (df.Latitude <= (x2 + 1000)) & (df.Longitude >= (y2 - 1000)) & (df.Longitude <= (y2 + 1000))].index)
            # areatotal = len(ddf.index)
            # print("area ticket ratio: " + str(areatotal / timetotal))
            ratio = (areatotal / timetotal)
            # print(ratio)
            # print(ddf)

            dictionary_data = {'time': time, 'lat': random_x, 'long': random_y, 'ratio': ratio}
            dictionarylist.append(dictionary_data)

    dictionary_df = pd.DataFrame.from_dict(dictionarylist)
    print(dictionary_df.sort_values("ratio"))

    parquetdataname = "C:/ticketdodger/python/data/test/testdata3.parquet"

    data_df = data_df.append(dictionary_df)
    data_df.to_parquet(parquetdataname)
    return data_df


print(timetest(24, 10000))


