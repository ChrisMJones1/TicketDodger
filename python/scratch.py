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
        parquetname = "data/tickets_" + starttime + "_to_" + endtime + ".parquet"
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


# def timetest(t):
#
#     df = pd.read_parquet("data/all_tickets.parquet")
#     lng_range = (abs(df.Longitude.max() - df.Longitude.min()))
#     lat_range = (abs(df.Latitude.max() - df.Latitude.min()))
#     print("Lng range = " + str(lng_range))
#     print("Lat range = " + str(lat_range))
#
#     lng_max = df.new_long.max()
#     lng_min = df.new_long.min()
#     lat_max = df.new_lat.max()
#     lat_min = df.new_lat.min()
#
#     print("Lng max = " + str(lng_max))
#     print("Lng min = " + str(lng_min))
#
#     print("Lat max = " + str(lat_max))
#     print("Lat min = " + str(lat_min))
#
# timetest(1)
#
# # the dictionary to pass to panda's dataframe
# dict = {}
#
# # a counter to use to add entries to "dict"
# i = 0
#
# # Example data to loop and append to a dataframe
# data = [{"foo": "foo_val_1", "bar": "bar_val_1"},
#        {"foo": "foo_val_2", "bar": "bar_val_2"}]
#
# # the loop
# for entry in data:
#
#     # add a dictionary entry to the final dictionary
#     dict[i] = {"col_1_title": entry['foo'], "col_2_title": entry['bar']}
#
#     # increment the counter
#     i = i + 1
#
# # create the dataframe using 'from_dict'
# # important to set the 'orient' parameter to "index" to make the keys as rows
# df = pd.DataFrame.from_dict(dict, "index")
#
# print(df)

# parquetdataname = "data/test/testdata4.parquet"
# df = pd.read_parquet(parquetdataname)

model = Sequential()
model.add(Dense(10, input_dim=3, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])

# model = tf.keras.models.load_model('proper_ticket_risk_modelv2.h5')

for j in range(5):
    print("loop " + str(j + 1))
    df = timetest(1, 1000)
    df = df.sort_values('ratio')
    # df = df.tail(400)
    print(df)

    target = df.pop('ratio')
    dataset = tf.data.Dataset.from_tensor_slices((df.values, target.values))

    print(df.shape)

    train_dataset = dataset.shuffle(len(df)).batch(1)
    # test_dataset = dataset.shuffle(len(df)).batch(0.3)


    # for feat, targ in dataset.take(5):
    #   print ('Features: {}, Target: {}'.format(feat, targ))
    #

    # # model loader
    # model = tf.keras.models.load_model('C:/ticketdodger/python/proper_ticket_risk_model.h5')
    model.fit(train_dataset, epochs=5, verbose=1)

    _, accuracy = model.evaluate(train_dataset)
    print('Accuracy: %.2f' % (accuracy * 100))


# def get_compiled_model():
#
#     model = tf.keras.Sequential([
#         tf.keras.layers.Dense(10, activation='relu'),
#         tf.keras.layers.Dense(10, activation='relu'),
#         tf.keras.layers.Dense(1)
#     ])
#
#     model.compile(optimizer='adam',
#                   loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
#                   metrics=['accuracy'])
#     return model
#
#
# model = get_compiled_model()
# model.fit(train_dataset, epochs=15)


# evaluate the keras model


model.save('downtown_ticket_risk_modelv2.h5')

# for feat, targ in dataset.take(5):
#   print ('Features: {}, Target: {}'.format(feat, targ))

# X = data[:, 0:3]
# y = data[:, 3]



# data.to_csv("./testdata.csv")

# data_total_len = data[data.columns[0]].size
# data_train_frac = 0.6
# split_index = math.floor(data_total_len*data_train_frac)
# training_data = data.iloc[:split_index]
# evaluation_data = data.iloc[split_index:]

# column_count = 4;
# label_column_index = 3 # Zero based index (so this is the 18th column)
#
# def preprocess(data):
#     X = data.iloc[:, 0:column_count-1]
#     y = data.iloc[:, label_column_index]
#     y = y-1 # shift label value range from 1-7 to 0-6



# print(timetest(24, 100))
