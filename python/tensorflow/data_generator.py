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
# TensorFlow and tf.keras
import tensorflow as tf
# Only necessary if you're using Keras (obviously)
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

import random
from tqdm import tqdm, trange

import math
import pprint as pp
from datetime import datetime

from itertools import product
from string import ascii_uppercase
from matplotlib import patheffects

from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler

def timetest(time_range, r):
    zero_count = 0
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
        parquetname = "../data/tickets_" + starttime + "_to_" + endtime + ".parquet"
        df = pd.read_parquet(parquetname)
        # Full data range
        # lng_range = 115529.80704000004
        # lat_range = 114956.93543999991
        # lng_max = 638458.22016  # State line meters 0405
        # lng_min = 522928.41312  # State line meters 0405
        # lat_max = 2027717.99688  # State line meters 0405
        # lat_min = 1912761.06144  # State line meters 0405
        # just downtown core
        lng_range = 49538.762
        lat_range = 37701.149
        lng_max = 572548.325  # State line meters 0405
        lng_min = 523009.563  # State line meters 0405
        lat_max = 1986392.399  # State line meters 0405
        lat_min = 1948691.250  # State line meters 0405

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
            if ratio == 0:
                zero_count += 1
            # print(ratio)
            # print(ddf)

            dictionary_data = {'time': time, 'lat': random_x, 'long': random_y, 'ratio': ratio}
            dictionarylist.append(dictionary_data)

    dictionary_df = pd.DataFrame.from_dict(dictionarylist)
    print(dictionary_df.sort_values("ratio"))

    # parquetdataname = "data/test/testdata4.parquet"

    data_df = data_df.append(dictionary_df)
    # data_df.to_parquet(parquetdataname)
    print("zero ratio = " + str(zero_count / (r * 24)))
    return data_df


# data_df = timetest(24, 10)
#
# print(data_df.std(axis = 0, skipna = True))

# generate 2d classification dataset
# example making new class predictions for a classification problem
from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
# generate 2d classification dataset
X, y = make_blobs(n_samples=100, centers=2, n_features=2, random_state=1)
scalar = MinMaxScaler()
scalar.fit(X)
X = scalar.transform(X)
# define and fit the final model
model = Sequential()
model.add(Dense(4, input_dim=2, activation='relu'))
model.add(Dense(4, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam')
model.fit(X, y, epochs=500, verbose=0)
# new instances where we do not know the answer
Xnew, _ = make_blobs(n_samples=3, centers=2, n_features=2, random_state=1)
Xnew = scalar.transform(Xnew)
# make a prediction
ynew = model.predict_classes(Xnew)
# show the inputs and predicted outputs
for i in range(len(Xnew)):
	print("X=%s, Predicted=%s" % (Xnew[i], ynew[i]))