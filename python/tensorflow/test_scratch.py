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
from keras.layers.advanced_activations import LeakyReLU

import random

from tensorflow_core.python.keras.layers import BatchNormalization
from tqdm import tqdm, trange

import math
import pprint as pp
from datetime import datetime

from itertools import product
from string import ascii_uppercase
from matplotlib import patheffects
import matplotlib.pyplot as plt

# import tracemalloc
#
# tracemalloc.start()

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
        # lng_range = 49538.762
        # lat_range = 37701.149
        lng_max = 572548.325  # State line meters 0405
        lng_min = 523009.563  # State line meters 0405
        lat_max = 1986392.399  # State line meters 0405
        lat_min = 1948691.250  # State line meters 0405
        lng_range = lng_max - lng_min
        lat_range = lat_max - lat_min
        grid_increment = 5
        lng_grids = math.ceil(lng_range / grid_increment)
        lat_grids = math.ceil(lat_range / grid_increment)

        for y in trange(r, desc="count loop"):
            #ddf = df
            # print("starting rep: " + str(y))
            random_x = random.random()
            random_y = random.random()
            x2 = (random_x * lat_grids * grid_increment) + lat_min

            # print("random lat: " + str(x2))
            y2 = (random_y * lng_grids * grid_increment) + lng_min
            # print("random long: " + str(y2))
            # timetotal = len(df.index)
            # print("len of df: " + str(timetotal))
            areatotal = len(df[(df.Latitude >= (x2 - 500)) & (df.Latitude <= (x2 + 500)) & (df.Longitude >= (y2 - 500)) & (df.Longitude <= (y2 + 500))].index)
            # areatotal = len(ddf.index)
            # print("area ticket ratio: " + str(areatotal / timetotal))
            ratio = (areatotal / 1133)
            if ratio == 0:
                zero_count += 1
            # if ratio > 0:
            #     ratio = 1
            # print(ratio)
            # print(ddf)

            dictionary_data = {'time': time, 'lat': random_x, 'long': random_y, 'ratio': ratio}
            dictionarylist.append(dictionary_data)

    dictionary_df = pd.DataFrame.from_dict(dictionarylist)
    print(dictionary_df.sort_values("ratio"))

    # parquetdataname = "data/test/testdata4.parquet"

    data_df = data_df.append(dictionary_df)
    # data_df.to_parquet(parquetdataname)
    print("zero ratio = " + str(zero_count / (r * time_range)))
    # remove all zero instances
    # data_df = data_df.tail((r * 24) - zero_count)
    return data_df



data_df = timetest(1, 1000)
data_df = data_df.sort_values('ratio')
target = data_df.pop('ratio')
target = target.values
print(data_df)
print(target)
test_array = np.array([[0.0, 0.519256, 0.351533]])


# dataset = tf.data.Dataset.from_tensor_slices(data_df.values)

new_model = tf.keras.models.load_model('../downtown_ticket_risk_modelv2.h5')

wrong_counter = 0
predictions = new_model.predict(data_df.values)

# show the inputs and predicted outputs
predictions = predictions[:, 0]
for i in range(len(predictions)):

    print("X=%s, Predicted=%s" % (target[i], predictions[i]))
    # print('%s => %d (expected %d)' % (data_df.values[i], predictions[i], target[i]))
    # if predictions[i] != target[i]:
    #     wrong_counter += 1
average_threshold = 0
high_count = 0
for i in range(len(predictions)):
    val = ''
    pred = ''
    if target[i] >= 0.01:
        val = 'high risk'
        # high_count += 1
        # average_threshold += predictions[i]

    # elif target[i] >= 0.001:
    #     val = 'medium risk'


    elif target[i] >= 0.0001:
        val = 'small risk'
        # high_count += 1
        # average_threshold += predictions[i]

    else:
        val = "no risk"
        high_count += 1
        average_threshold += predictions[i]

    if predictions[i] >= 0.005:
        pred = 'high risk'

    # elif predictions[i] >= 0.003:
    #     pred = 'medium risk'

    elif predictions[i] >= 0.001:
        pred = 'small risk'

    else:
        pred = "no risk"

    print("X=%s, Predicted=%s" % (val, pred))
    if(val == pred):
        wrong_counter += 1

print('correct answer ratio = ' + str(wrong_counter))

print("average value of high rating = " + str(average_threshold / high_count))

print("mean of predictions: " + str(np.mean(predictions)))
print("SD of predictions: " + str(np.std(predictions)))
print("mean of values: " + str(np.mean(target)))
print("std of values: " + str(np.std(target)))

# plt.show()

# print("expected value = 0.050891")
# print("actual value = ")
# print(predictions)
#
# test_array = np.array([[0.0, 0.517082, 0.367158]])
#