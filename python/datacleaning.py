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

from datetime import datetime

# hmap = folium.Map(location=[34, -118], zoom_start=9)


from itertools import product
from string import ascii_uppercase
from matplotlib import patheffects

# plt.style.use('seaborn')

# plt.close('all')

inProj = Proj("esri:102645", preserve_units=False)
outProj = Proj("epsg:4326") # WGS84 in lat long
y1, x1 =  (560301.731, 1976879.710)
print(transform(inProj,outProj,x1,y1))

# minlat = 1949576.119
# maxlat = 1994404.782
# minlong = 528562.621
# maxlong = 567940.440

# Center LA 34°02'36.1"N 118°15'01.4"W 34.04336111111111 -118.25038888888889
# minlat = 1976879.710 - 500
# maxlat = 1976879.710 - 250
# minlong = 560301.731 - 500
# maxlong = 560301.731 - 250

df = pd.read_csv("Parking_Citations.csv", parse_dates=[1], dtype={"Ticket_number": object, "Issue_time": object, "Latitude": float, "Longitude": float})


df = df.dropna(how='any')
df.astype({'Issue_time': 'object'}).dtypes
df['Issue_time'] = df['Issue_time'].apply(lambda x: str(x).zfill(4))
df['Issue_time'] = pd.to_datetime(df['Issue_time'], format='%H%M').dt.time
df.sort_values(by='Latitude', ascending=False)

# apply the filter to filter out all the bad results (which are value 99999)
df_floorfilter = df['Latitude'] > 99999
df = df[df_floorfilter]

# Filter time
# ts = df['Issue_time']
# df_longfiltermin = (ts.between_time('12:00', '13:00'))
# df = df[df_longfiltermin]


# Convert to Meters instead
df['Latitude'] = df['Latitude'].apply(lambda x: x * 0.3048)
df['Longitude'] = df['Longitude'].apply(lambda x: x * 0.3048)

df['new_lat'], df['new_long'] = transform(inProj, outProj, df["Latitude"].tolist(), df["Longitude"].tolist())
print("converted to lat long")
# x = df['new_lat'].values
# y = df['new_long'].values

# for x in range(1):
#     # hmap = folium.Map(location=[34, -118], zoom_start=9, tiles="cartodbdark_matter")
#     print("starting time range: " + str(x))
#     # starttime = (str(x) + "00").zfill(4)
#     # endtime = starttime[:2] + "59"
#     df_time = df
#     # mapname = "dark_timeheatmap_" + starttime + "_to_" + endtime + ".html"
#     # parquetname = "./mintickets_" + starttime + "_to_" + endtime + ".parquet"
#     parquetname = "./data/all_tickets.parquet"
#     # start = datetime.strptime(starttime, '%H%M').time()
#     # end = datetime.strptime(endtime, '%H%M').time()
#     #
#     # df_longfiltermin = (df_time['Issue_time'] <= end)
#     # df_time = df_time[df_longfiltermin]
#     # df_longfiltermax = (df_time['Issue_time'] >= start)
#     # df_time = df_time[df_longfiltermax]
#
#     # df_time = df_time.drop(columns=['Ticket_number', 'Issue_Date', 'Issue_time'])
#
#     df_time = df_time.reset_index(drop=True)
#
#     df_time.to_parquet(parquetname)
#     # x = df_time['new_lat'].values
#     # y = df_time['new_long'].values
#     #
#     # mapdata = np.transpose([x, y])
#     #
#     # print("transposed to mapdata")
#     #
#     # hm_wide = HeatMap(mapdata, radius=10, blur=18, min_opacity=0.2, max_opacity=0.8).add_to(hmap)
#     #
#     # print("hm wide created")
#     #
#     # hmap.save(mapname)


# # Group the xy into 2x2km grid squares by subtracting the minimum value of the axis, then dividing by the grid
# # size and rounding down
# df['Latitude'] = df['Latitude'].apply(lambda x: np.floor(((x - 1912761.06144)/2000)))
# df['Longitude'] = df['Longitude'].apply(lambda x: np.floor(((x - 522928.41312)/2000)))
#
# #convert into ints
# df['Latitude'] = df['Latitude'].astype('int')
# df['Longitude'] = df['Longitude'].astype('int')
# # Narrow down longitude values to just downtown core
# # df_longfiltermin = (df['Longitude'] < 3)
# # df = df[df_longfiltermin]
# # df_longfiltermax = (df['Longitude'] < maxlong)
# # df = df[df_longfiltermax]
#
# # Narrow down latitude values to just downtown core
# # df_latfiltermin = (df['Latitude'] > minlat)
# # df = df[df_latfiltermin]
# # df_latfiltermax = (df['Latitude'] < maxlat)
# # df = df[df_latfiltermax]
#
# df = df.reset_index(drop=True)
print(df.head())
print("///////////")
print("Total Number of Entries: ")
print(len(df.index))
print("////////////")
print("Boundaries: ")
print("minimum Latitude: ")
print(df['Latitude'].min())
print("maximum Latitude: ")
print(df['Latitude'].max())
print("minimum Longitude: ")
print(df['Longitude'].min())
print("maximum Longitude: ")
print(df['Longitude'].max())
#
# # print("/////////////")
# # print("500m grid squares tall: ")
# # print((df['Longitude'].max() - df['Longitude'].min()))
# # print("500M grid squares wide: ")
# # print((df['Latitude'].max() - df['Latitude'].min()))
#
# # ax = df.plot.scatter(x='Latitude', y='Longitude')
# # ay = plt.gca().invert_yaxis()
#
# # sns.kdeplot(df.Latitude, df.Longitude, cmap="Reds", shade=True)
# #
# # plt.show()
#
# # df_longfiltermax = (df['Longitude'] < newmin)
# # df = df[df_longfiltermax]
# #
# # # Narrow down latitude values to just downtown core
# # df_latfiltermin = (df['Latitude'] > newmax)
# # df = df[df_latfiltermin]
#
# # print(df.head())
# # print(len(df.index))
#
# df['count'] = df.groupby('Latitude')['Longitude'].transform('nunique')
# ddf = df.drop(columns = ['Ticket_number', 'Issue_Date', 'Issue_time'])
# # print(ddf)
# ddf = ddf.drop_duplicates()
# # convert grids back to meters
# ddf['new_lat'] = df['Latitude'].apply(lambda x: ((x * 2000) + 1912761.06144))
# ddf['new_long'] = df['Longitude'].apply(lambda x: ((x * 2000) + 522928.41312))
#
# ddf['new_lat'], ddf['new_long'] = transform(inProj, outProj, ddf["new_lat"].tolist(), ddf["new_long"].tolist())
# # x = ddf['Latitude'].values
# # y = ddf['Longitude'].values
# # z = ddf['count'].values
#
#
# #print(ddf.sort_values(['Latitude', 'Longitude']))
# # print(ddf)
# # sns.heatmap(ddf, annot=True, fmt="d", linewidths=.5)
#
# x = ddf['new_lat'].values
# y = ddf['new_long'].values
# z = ddf['count'].values
# max_amount = float(ddf['count'].max())
#
#
# def floatconvert(b):
#     return float(b)
#
#
# def floatscaleconvert(b):
#     return (float(b) / 29.0)
#
#
# bulkfloatconvert = np.vectorize(floatconvert)
# bulkfloatscaleconvert = np.vectorize(floatscaleconvert)
#
# x = bulkfloatconvert(x)
# y = bulkfloatconvert(y)
# z = bulkfloatscaleconvert(z)
#
# mapdata = np.transpose([x, y, z])




# fig, (ax, ax2)=plt.subplots(ncols=2)
# ax.set_title("tripcolor")
# ax.tripcolor(list(x), list(y), list(z))
# ax2.set_title("tricontour")
# ax2.tricontourf(list(x), list(y), list(z))

# Calculate the point density
# xy = np.vstack([list(x), list(y)])
# print("past vstack")
# z = gaussian_kde(xy)(xy)
# print("past kde")
# fig, ax = plt.subplots()
# print("past subplots")
# ax.scatter(list(x), list(y), c=z, s=100, edgecolor='')
# print("past scatter")
# plt.pcolor(df)
# print("Past pcolor")
# plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
# plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)

# ax = plt.imshow(ddf, interpolation='nearest', cmap='Oranges').axes
#
#
# ax.grid('off')
# ax.xaxis.tick_top()

# sns.scatterplot(list(x), list(y), list(z), None, list(z))
#
# plt.show()
# print(ddf.Latitude)

