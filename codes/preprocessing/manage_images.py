from remap import remap
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import geopandas as gpd
from PIL import Image


gdf = gpd.read_file('shapefiles/estadosl_2007.shp')
gdf.head()

for hour in [str(hour).zfill(2) for hour in range(23, 24)]:
    path = "/home/adriano/CAP-351/project/store/nc/noaa-goes16/ABI-L2-CMIPF/2019/338/%s"%hour
    minutes = os.listdir(path)

    def resize(filename, size=128):
        img = Image.open(filename)
        img = img.resize((size, size))
        img.save(filename)

    for minute in minutes:
        path_temp = os.path.join(path, minute)
        file = list(filter(lambda x: x.endswith('.nc'), os.listdir(path_temp)))
        if len(file) < 1:
            continue
        file = file[0]
        time = path.split('/')
        time = '%s_%s_%s'%(time[-2], time[-1], minute)
        for _, row in gdf.iterrows():
            uf = row.SIGLAUF3
            bbox = row.geometry.bounds
            grid = remap(path=os.path.join(path_temp, file), resolution=2, extent=bbox, driver='NETCDF4')
            grid = grid.ReadAsArray()
            fig, ax = plt.subplots(figsize=(10, 10))
            if not os.path.exists('new_images/'+uf):
                os.makedirs('new_images/'+uf)
            ax.imshow(grid, cmap='gray')
            ax.set_xticks([]); plt.yticks([])
            filename = 'new_images/%s/%s__%s__%s.png'%(uf, uf, int(grid.mean()), time)
            plt.savefig(filename, bbox_inches='tight', transparent="False", pad_inches=0)
            resize(filename)
        