from netCDF4 import Dataset, num2date
from pathlib import Path
import pandas as pd
#import datetime as dt
import numpy as np
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import matplotlib.pyplot as plt

'''
To run basemap you need to install PROJ4 and GEOS(put it in the path).

Todos os demais pacotes devem ser instalados/atualizados utilizando o comando 'conda install/update'

netCDF4 deve ser instalado utilizando pip install

Deve-se especificar a variável de ambiente PROJ_LIB

Basemap foi baixado vs1.2.1 (.whl) e depois instalado via linha de comando

Tinha 2 versões de numpy ao mesmo tempo: desinstalei tudo (matplotlib; numpy; pandas -> conda uninstall e pip uninstall várias vezes)
e instalei tudo novamente utilizando conda install. Por fim instalei pyproj com o conda

Depois desses passos finalmente voltou a funcionar. Mas deu erro novamente.

Por fim, instalei com o conda e desinstalei novamente do conda/pip/pip3. 
Limpei o cache do anaconda. INSTALEI CADA COMPONENTE UTILIZANDO O PIP e voltou a funcionar


'''

nasa_path = Path(r"C:\Users\lucas\PycharmProjects\Files")

nc = Dataset(nasa_path.joinpath("MERRA2_400.tavg1_2d_slv_Nx.20190801.nc4"), mode='r')

## All variables
for i in nc.variables:
    print (i, nc.variables[i].shape)

variable = "T2M"

#Extracting data from netCDF file
lats = nc.variables['lat'][:]
lons = nc.variables['lon'][:]
data = nc.variables[variable][:]
time = num2date(nc.variables['time'][:], nc.variables['time'].units)

# Plotting
fig = plt.figure(figsize=(16,9))
fig.subplots_adjust(left=0, right=1, bottom=0, top=0.9)

m = Basemap(projection='moll', llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=0, urcrnrlon=360, resolution='c', lon_0=0)

m.drawcoastlines()
m.drawmapboundary()

# Make the plot continuous
data_cyclic, lons_cyclic = addcyclic(data[0, :, :], lons) #00:30H
# Shift the grid so lons go from -180 to 180 instead of 0 to 360.
data_cyclic, lons_cyclic = shiftgrid(180., data_cyclic, lons_cyclic, start=False)
# Create 2D lat/lon arrays for Basemap
lon2d, lat2d = np.meshgrid(lons_cyclic, lats)
# Transforms lat/lon into plotting coordinates for projection
x, y = m(lon2d, lat2d)
# Plot of air temperature with 11 contour intervals
cs = m.contourf(x, y, data_cyclic, 11, cmap=plt.set_cmap('Spectral_r'))
cbar = plt.colorbar(cs, orientation='horizontal', shrink=0.5)
cbar.set_label("%s (%s)" % (nc.variables[variable].standard_name,
                            nc.variables[variable].units))
plt.title("%s on %s" % (nc.variables[variable].standard_name, time[0]))
plt.show()