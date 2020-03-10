from flask import Flask, request, render_template, jsonify, send_from_directory, url_for
import requests
import numpy as np
import pandas as pd

# from flask_cors import CORS


import pyarrow
from datetime import datetime

# import os
# os.environ['PATH']


app = Flask(__name__, static_folder='../')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index2.0.html')
# CORS(app)

# @app.route('/')
# def index():
#     return "Hello, World!"

#
# @app.route('/')
# def index():
#     return print('connected')

@app.route('/result')
def result():
    return send_from_directory(app.static_folder, 'result.html')

@app.route('/map', methods=['POST'])
def process():
    bounds = request.get_json(force=True)

    starttime = (str(bounds['time']) + "00").zfill(4)
    endtime = starttime[:2] + "59"
    parquetname = "C:/ticketdodger/python/data/mini/mintickets_" + starttime + "_to_" + endtime + ".parquet"
    df = pd.read_parquet(parquetname)
    cache_df = df
    # new_df = df;
    # cache_df = df;
    # print(df)

    # print(bounds)
    try:
        minlat = bounds['latlng']['_southWest']['lat']
    except TypeError:
        print(bounds)
        print(bounds['_southWest'])
    maxlat = bounds['latlng']['_northEast']['lat']
    minlong = bounds['latlng']['_southWest']['lng']
    maxlong = bounds['latlng']['_northEast']['lng']
    # print("min long = " + str(minlong))
    # print("max long = " + str(maxlong))
    #
    # print("min lat = " + str(minlat))
    # print("max lat = " + str(maxlat))

    df_longfiltermin = (df['new_long'] >= minlong)
    df = df[df_longfiltermin]
    df_longfiltermax = (df['new_long'] <= maxlong)
    df = df[df_longfiltermax]

    # print(df)

    df_latfiltermin = (df['new_lat'] >= minlat)
    df = df[df_latfiltermin]
    df_latfiltermax = (df['new_lat'] <= maxlat)
    df = df[df_latfiltermax]

    #do the same, but grab the cached entries

    try:
        minlat = bounds['cache']['_southWest']['lat']
    except TypeError:
        print(bounds)
        print(bounds['_southWest'])
    maxlat = bounds['cache']['_northEast']['lat']
    minlong = bounds['cache']['_southWest']['lng']
    maxlong = bounds['cache']['_northEast']['lng']
    # print("min long = " + str(minlong))
    # print("max long = " + str(maxlong))
    #
    # print("min lat = " + str(minlat))
    # print("max lat = " + str(maxlat))

    df_longfiltermin = (cache_df['new_long'] >= minlong)
    cache_df = cache_df[df_longfiltermin]
    df_longfiltermax = (cache_df['new_long'] <= maxlong)
    cache_df = cache_df[df_longfiltermax]

    # print(df)

    df_latfiltermin = (cache_df['new_lat'] >= minlat)
    cache_df = cache_df[df_latfiltermin]
    df_latfiltermax = (cache_df['new_lat'] <= maxlat)
    cache_df = cache_df[df_latfiltermax]

    df = (pd.merge(df, cache_df, indicator=True, how='outer')
         .query('_merge=="left_only"')
         .drop('_merge', axis=1))
    # print(df)

    x = df['new_lat'].values
    y = df['new_long'].values

    mapdata = np.transpose([x, y]).tolist()
    # print(mapdata)

    return jsonify({'latlongs': mapdata})
    # output = firstName + lastName
    # if firstName and lastName:
    #     return jsonify({'output':'Full Name: ' + output})

    return jsonify({'error' : 'Missing data!'})



@app.route('/search', methods=['POST'])
def search():
    bounds = request.get_json(force=True)

    starttime = (str(bounds['time']) + "00").zfill(4)
    endtime = starttime[:2] + "59"
    parquetname = "C:/ticketdodger/python/data/mini/mintickets_" + starttime + "_to_" + endtime + ".parquet"
    df = pd.read_parquet(parquetname)


    try:
        minlat = bounds['latlng']['_southWest']['lat']
    except TypeError:
        print(bounds)
        print(bounds['_southWest'])
    maxlat = bounds['latlng']['_northEast']['lat']
    minlong = bounds['latlng']['_southWest']['lng']
    maxlong = bounds['latlng']['_northEast']['lng']
    # print("min long = " + str(minlong))
    # print("max long = " + str(maxlong))
    #
    # print("min lat = " + str(minlat))
    # print("max lat = " + str(maxlat))

    df_longfiltermin = (df['new_long'] >= minlong)
    df = df[df_longfiltermin]
    df_longfiltermax = (df['new_long'] <= maxlong)
    df = df[df_longfiltermax]

    # print(df)

    df_latfiltermin = (df['new_lat'] >= minlat)
    df = df[df_latfiltermin]
    df_latfiltermax = (df['new_lat'] <= maxlat)
    df = df[df_latfiltermax]

    x = df['new_lat'].values
    y = df['new_long'].values

    mapdata = np.transpose([x, y]).tolist()
    # print(mapdata)

    return jsonify({'latlongs': mapdata})
    # output = firstName + lastName
    # if firstName and lastName:
    #     return jsonify({'output':'Full Name: ' + output})

    return jsonify({'error' : 'Missing data!'})

if __name__ == '__main__':
    app.run(debug=True)