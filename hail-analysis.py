import os
from remap import remap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
import geopandas as gpd
from cpt_convert import loadCPT
from matplotlib.colors import LinearSegmentedColormap
from shapely.geometry import Polygon, Point

from oct2py import Oct2Py

days = [297]
hours = np.arange(24)
channels = [13]
shp = gpd.read_file('./shapefiles/estadosl_2007.shp')
shp = shp[shp['SIGLAUF3'] == 'SP']
bbox = shp.bounds.values[0]
poly = shp.geometry.values[0]
    
for day in days:
    for hour in hours:
        path = 'noaa-goes16/ABI-L2-CMIPF/2019/%s/%s'%(day, str(hour).zfill(2))
        files = [os.path.join(path, file) for file in os.listdir(path)]    
        files = list(filter(lambda x: x.endswith('.nc'), files))
        
        for file in files:
            channel = file.split('/')[-1][19:21]
            year = file.split('/')[-1][27:31]
            day = file.split('/')[-1][31:34]
            hour = file.split('/')[-1][34:36]
            minute = file.split('/')[-1][36:38]
            
            plt.figure(figsize=(17, 10))
            plt.title('GOES-16 ABI CANAL %s - %sº dia de %s às %s:%s'%(channel, 
                                                                       day, 
                                                                       year, 
                                                                       hour, 
                                                                       minute))
            b = Basemap(projection='merc', llcrnrlon=bbox[0], llcrnrlat=bbox[1]
                        ,urcrnrlon=bbox[2], urcrnrlat=bbox[3])
            b.readshapefile('./shapefiles/estadosl_2007', name='sp', 
                            linewidth=2, color='red')
            cpt = loadCPT('./IR4AVHRR6.cpt')
            cpt_convert = LinearSegmentedColormap('cpt', cpt)
            
            data = remap(file, bbox, 1, 'netCDF')
            grid = data.ReadAsArray()
            
            lons = np.linspace(bbox[0], bbox[2], grid.shape[1])
            lats = np.linspace(bbox[1], bbox[3], grid.shape[0])
            
            for lat, i in zip(lats, range(grid.shape[0])):
                for lon, j in zip(lons, range(grid.shape[1])):
                    point = Point(lon, lat)
                    print(i, ', ', j, ': ', point)
                    if not poly.contains(point):
                        grid[i][j] = np.nan
            
            b.drawmeridians(np.linspace(bbox[0], bbox[2], 10), labels=[False, 
                            False, False, True], fmt='%.2f', 
            labelstyle='+/-', color='k')
            b.drawparallels(np.linspace(bbox[1], bbox[3], 10), 
                            labels=[True, False, False, False], fmt='%.2f', 
                            labelstyle='+/-', color='k')
            
            cmap = b.imshow(grid,  origin='upper', vmin=200, vmax=300, 
                            cmap=cpt_convert)
            cbar = b.colorbar(cmap, extend='both', label='Temperatura [K]')
            
            inside = plt.axes([.17, .18, .20, .20])
            inside.hist(grid.reshape(1, -1)[0], bins=100, color='k', alpha=.9)
            inside.set_xlabel('Temperatura [K]', color='w')
            inside.set_yticks([])
            inside.tick_params(colors='w')
        
#            plt.show('hail/goes16-CH%s-%s-%s-%s-%s.png'%(channel, year, day, hour, minute))
            plt.show()







#path = 'noaa-goes16/ABI-L2-CMIPF/2019/297/'
#for hour in sorted(os.listdir(path)):
#    p = os.path.join(path, hour)
#    files = list(filter(lambda x: x.endswith('.nc'), os.listdir(p)))
#    files = [os.path.join(p, file) for file in files]
##    print(files)
#    for file in files:
#        if not 'C13' in file:
#            continue
#        
#        shp = gpd.read_file('./shapefiles/estadosl_2007.shp')
#        shp = shp[shp['SIGLAUF3'] == 'SP']
#        bbox = shp.bounds.values[0]
#        
#        channel = file.split('/')[-1][19:21]
#        year = file.split('/')[-1][27:31]
#        day = file.split('/')[-1][31:34]
#        hour = file.split('/')[-1][34:36]
#        minute = file.split('/')[-1][36:38]
#        plt.figure(figsize=(17, 10))
#        
#        plt.title('GOES-16 ABI CANAL %s - %sº dia de %s às %s:%s'%(channel, day, year, hour, minute))
#        b = Basemap(projection='merc', llcrnrlon=bbox[0], llcrnrlat=bbox[1], 
#                    urcrnrlon=bbox[2], urcrnrlat=bbox[3])
#        b.readshapefile('./shapefiles/estadosl_2007', name='sp', linewidth=2, color='red')
#            
#        cpt = loadCPT('./IR4AVHRR6.cpt')
#        cpt_convert = LinearSegmentedColormap('cpt', cpt)
#        
#        data = remap(file, bbox, 1, 'netCDF')
#        grid = data.ReadAsArray()
#        
#        lons = np.linspace(bbox[0], bbox[2], grid.shape[1])
#        lats = np.linspace(bbox[1], bbox[3], grid.shape[0])
#        
#        b.drawmeridians(np.linspace(bbox[0], bbox[2], 10), labels=[False, False, False, True], 
#                        fmt='%.2f', labelstyle='+/-', color='k')
#        b.drawparallels(np.linspace(bbox[1], bbox[3], 10), labels=[True, False, False, False], 
#                        fmt='%.2f', labelstyle='+/-', color='k')
#        
#        cmap = b.imshow(grid,  origin='upper', vmin=200, vmax=300, cmap=cpt_convert)
#        cbar = b.colorbar(cmap, extend='both', label='Temperatura [K]')
#        inside = plt.axes([.17, .18, .20, .20])
#        
#        inside.hist(grid.reshape(1, -1)[0], bins=100, color='k', alpha=.9)
#        inside.set_xlabel('Temperatura [K]', color='w')
#        inside.set_yticks([])
#        inside.tick_params(colors='w')
#        
#        plt.savefig('hail/goes16-CH%s-%s-%s-%s-%s.png'%(channel, year, day, hour, minute))