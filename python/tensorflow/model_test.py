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

parquetdataname = "C:/ticketdodger/python/data/test/testdata2.parquet"
data_df = pd.read_parquet(parquetdataname)
data_df = data_df.sort_values('ratio')
target = data_df.pop('ratio')
target = target.values
print(data_df)
print(target)
test_array = np.array([[0.0, 0.519256, 0.351533]])


# dataset = tf.data.Dataset.from_tensor_slices(data_df.values)

new_model = tf.keras.models.load_model('C:/ticketdodger/python/proper_ticket_risk_model.h5')


predictions = new_model.predict(data_df.values)

# show the inputs and predicted outputs
for i in range(len(predictions)):
    print("X=%s, Predicted=%s" % (target[i], predictions[i]))
# print("expected value = 0.050891")
# print("actual value = ")
# print(predictions)
#
# test_array = np.array([[0.0, 0.517082, 0.367158]])
#
#
# predictions = new_model.predict(test_array)
#
# print("expected value = 0.025894")
# print("actual value = ")
# print(predictions)
#
# test_array = np.array([[0.0, 0.995078, 0.049947]])
#
#
# predictions = new_model.predict(test_array)
#
# print("expected value = 0.00000")
# print("actual value = ")
# print(predictions)
