# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import gaussian_kde
# import seaborn as sns
from pyproj import Proj, transform
# import folium
# from folium.plugins import HeatMap
# import geopandas as gpd
# import pyarrow

from datetime import datetime

# hmap = folium.Map(location=[34, -118], zoom_start=9)


from itertools import product
from string import ascii_uppercase
from matplotlib import patheffects

# plt.style.use('seaborn')

# plt.close('all')

inProj = Proj("esri:102645", preserve_units=False)
outProj = Proj("epsg:4326") # WGS84 in lat long
# y1, x1 =  (560301.731, 1976879.710)
# print(transform(inProj,outProj,x1,y1))

# Center LA 34°02'36.1"N 118°15'01.4"W 34.04336111111111 -118.25038888888889
# minlat = (1976879.710  - 1250)
# maxlat = (1976879.710 + 1250)
# minlong = (560301.731  - 1250)
# maxlong = (560301.731 + 1250)

# Full mapping bounds
minlat = 1912761.06144
maxlat = 2027717.99688
minlong = 522928.41312
maxlong = 638458.22016
#	33.7030139, -118.9409686
# 34.7478410, -117.6972698

y1, x1 = (minlong, maxlat)
print(transform(inProj, outProj, x1, y1))

y2, x2 = (maxlong, maxlat)
print(transform(inProj, outProj, x2, y2))
