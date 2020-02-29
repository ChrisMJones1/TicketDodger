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


import math
import pprint as pp
from datetime import datetime

from itertools import product
from string import ascii_uppercase
from matplotlib import patheffects

# import tracemalloc
#
# tracemalloc.start()


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

parquetdataname = "C:/ticketdodger/python/data/test/testdata3.parquet"
df = pd.read_parquet(parquetdataname)

target = df.pop('ratio')
dataset = tf.data.Dataset.from_tensor_slices((df.values, target.values))

print(df.shape)

train_dataset = dataset.shuffle(len(df)).batch(1)


# for feat, targ in dataset.take(5):
#   print ('Features: {}, Target: {}'.format(feat, targ))
#
# model = Sequential()
# model.add(Dense(4, input_dim=3, activation='relu'))
# model.add(Dense(4, activation='relu'))
# model.add(Dense(1, activation='sigmoid'))
#
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model = tf.keras.models.load_model('C:/ticketdodger/python/proper_ticket_risk_model.h5')
model.fit(train_dataset, epochs=50)


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
_, accuracy = model.evaluate(train_dataset)
print('Accuracy: %.2f' % (accuracy*100))

model.save('proper_ticket_risk_model.h5')

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
