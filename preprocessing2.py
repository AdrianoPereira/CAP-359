import os
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point


path = 'noaa-goes16/GLM-L2-LCFA/2019/297'
hours = sorted(os.listdir(path))
product = ['flash']
# variables = ['_id', '_lat', '_lon', '_area', '_energy', '_quality_flag',
#              '_time_offset_of_first_event', '_time_offset_of_last_event',
#              '_frame_time_offset_of_first_event', '_frame_time_offset_of_last_event']
variables = ['_lat', '_lon']

data = {}
data['start_scan'] = []
data['end_scan'] = []
data['year'] = []
data['julian_day'] = []
data['hour'] = []
data['minute'] = []
data['flash_lon'] = []
data['flash_lat'] = []
data['geometry'] = []


for hour in hours[:2]:
    files = sorted(os.listdir(os.path.join(path, hour)))
    files = list(filter(lambda x: x.endswith('.nc'), files))

    for file in files[:5]:
        start_scan = file[20:34]
        end_scan = file[36:50]
        y = start_scan[:4]
        jd = start_scan[4:7]
        h = start_scan[7:9]
        m = start_scan[9:11]

        file = os.path.join(os.path.join(path, hour), file)

        nc = Dataset(file, 'r')

        lons, lats = nc.variables['flash_lon'], nc.variables['flash_lat']

        for lon, lat in zip(lons, lats):
            point = Point(lon, lat)

            data['start_scan'].append(start_scan)
            data['end_scan'].append(end_scan)
            data['year'].append(y)
            data['julian_day'].append(jd)
            data['hour'].append(h)
            data['minute'].append(m)
            data['flash_lon'].append(lon)
            data['flash_lat'].append(lat)
            data['geometry'].append(point)

    break

if __name__ == "__main__":

    df = pd.DataFrame(data)

    df.to_csv('/home/adriano/obt/data.csv', index=False)
