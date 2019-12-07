import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
import os
import scipy.interpolate
import geopandas as gpd
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable


def get_coords(files, bounds):
    minx, maxx = bounds.minx.values[0], bounds.maxx.values[0]
    miny, maxy = bounds.miny.values[0], bounds.maxy.values[0]
    lats, lons = [], []
    for file in files:
        nc = Dataset(file)
        for lat, lon in zip(nc.variables['flash_lat'][:],
                            nc.variables['flash_lon'][:]):
            if (lat >= miny and lat <= maxy) and (lon >= minx and lon <= maxx):
                lats.append(lat);
                lons.append(lon)
    return lats, lons


if __name__ == "__main__":
    # for hour in np.arange(24):
    hour = 0
    path = './noaa-goes16/GLM-L2-LCFA/2019/301/%s'%(str(hour).zfill(2))
    files = [os.path.join(path, file) for file in os.listdir(path)]
    gdf = gpd.read_file('shapefiles/estadosl_2007.shp')
    sp = gdf[gdf['NOMEUF2'] == 'SAO PAULO']
    bounds = sp.bounds

    lats, lons = get_coords(files, bounds)

    fig, ax = plt.subplots(1, 2, figsize=(15, 8))
    grid = 50
    lon_grid = np.linspace(bounds.minx, bounds.maxx, grid)
    lat_grid = np.linspace(bounds.miny, bounds.maxy, grid)
    sp.plot(ax=ax[0], facecolor='None', edgecolor='k', linewidth=2)

    for i in range(grid - 1):
        for j in range(grid - 1):
            xy = (lon_grid[j][0], lat_grid[i][0])
            w = abs(lon_grid[j + 1] - lon_grid[j])[0]
            h = abs(lat_grid[i + 1] - lat_grid[i])[0]
            rec = patches.Rectangle(xy=xy, width=w, height=h, linewidth=1, alpha=0.1,
                                    edgecolor='r', facecolor='None')
            ax[0].add_patch(rec)
    ax[0].scatter(lons, lats)

    mat = np.zeros(shape=(grid, grid))
    for r in range(grid - 1):
        for c in range(grid - 1):
            count = 0
            minx, maxx = lon_grid[c], lon_grid[c + 1]
            miny, maxy = lat_grid[r], lat_grid[r + 1]
            for z in range(len(lats)):
                if (lats[z] >= miny and lats[z] <= maxy) and (lons[z] >= minx and lons[z] <= maxx):
                    mat[r][c] += 1

    minx, maxx = bounds.minx.values[0], bounds.maxx.values[0]
    miny, maxy = bounds.miny.values[0], bounds.maxy.values[0]
    cmap = ax[1].imshow(np.flip(mat, axis=0), extent=[minx, maxx, miny, maxy],
                        interpolation='gaussian', cmap='YlGn')
    fig.colorbar(cmap, orientation='horizontal')
    sp.plot(ax=ax[1], facecolor='None', edgecolor='k', linewidth=2)

    for i in range(grid - 1):
        for j in range(grid - 1):
            xy = (lon_grid[j][0], lat_grid[i][0])
            w = abs(lon_grid[j + 1] - lon_grid[j])[0]
            h = abs(lat_grid[i + 1] - lat_grid[i])[0]
            rec = patches.Rectangle(xy=xy, width=w, height=h, linewidth=1, alpha=0.1,
                                    edgecolor='r', facecolor='None')
            ax[1].add_patch(rec)
    plt.show('fig-{}.png'.format(str(hour).zfill(2)))

