import os
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point


def get_allfiles(days):
    data = []
    for day in days:
        path = 'noaa-goes16/GLM-L2-LCFA/2019'
        hours = os.listdir(os.path.join(path, day))
        hours = [os.path.join(os.path.join(path, day), h) for h in hours]
        for hour in hours:
            files = os.listdir(hour)
            files = [os.path.join(hour, file) for file in files]
            for file in files:
                data.append(file)
    return sorted(data)


def aggregate_by_time(days, minutes=15):
    data = get_allfiles(days)
    step = 3*minutes
    ans = {}
    for x in range(0, len(data)-step, step):
        key = str(x)
        ans[key] = []
        for y in range(x, x+step):
            ans[key].append(data[y])
    for y in range(len(data)-step, len(data)):
        ans[key].append(data[y])

    return ans


def save_aggregate(ans):
    for key in ans.keys():
        files = sorted(ans[key])
        f1 = files[0].split('/')[-1][20:34]
        f2 = files[-1].split('/')[-1][20:34]
        filename = 'GLM-FLASH-%s-%s.csv'%(f1, f2)

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

        for file in files:
            nc = Dataset(file, 'r')
            file = file.split('/')[-1]

            start_scan = file[20:34]
            end_scan = file[36:50]
            y = start_scan[:4]
            jd = start_scan[4:7]
            h = start_scan[7:9]
            m = start_scan[9:11]

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

        df = pd.DataFrame(data)
        df.to_csv('data/'+filename, index=False)


if __name__ == "__main__":
    days = [297]; days = list(map(str, days))

    data = aggregate_by_time(days)
    save_aggregate(data)

