import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import ListedColormap
from DataSet import DataSet

#class that just groups all different plot types together
class Plot(object):


    #display height plot, so just a line plot
    @staticmethod
    def heightPlot(data, dim_x,dim_y, ax, title=None, xlabel=None, ylabel=None, ticks=False):
        #in the x direction, we create equally spaced values from the minimal to the maximal height
        x = np.array(range(data.ZMIN, data.ZMAX, (data.ZMAX + data.ZMIN) // data.ZDIM))
        #in the y direction, we find all the corresponding data values to x
        y = [data.getRecord(dim_x, dim_y, i) for i in range(data.ZDIM)]
        #plot to axis and set the attributes
        ax.plot(x, y)
        if title:
            ax.set_title(title)
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if not ticks:
            ax.set_xticklabels([])


    #display stacked plots heightPlots
    @staticmethod
    def stackedPlot(anz_hours, x, y, ax):
        #instanciate all the needed DataSets and call heightPlot for them, with or without stylng values like title, xlabel etc.
        data_bundle = []
        for i in range(anz_hours):
            data_bundle.append(DataSet("temperature", i + 1))
            if i == 0:
                Plot.heightPlot(data_bundle[i], x, y, ax[i], title="Temperature at location (200,250) from hour 1 to 5")
            elif i == anz_hours // 2:
                Plot.heightPlot(data_bundle[i], x, y, ax[i], ylabel="Temperature (°C)")
            elif i == anz_hours:
                Plot.heightPlot(data_bundle[i], x, y, ax[i], xlabel="Height (m)", ticks=True)
            else:
                Plot.heightPlot(data_bundle[i], x, y, ax[i])

    #Creates a contour plot on top of a real world map
    @staticmethod
    def contourplotPlot(data, ax, height=1000,):
        #find z value according to hight in meters
        z = round(height/((data.ZMAX+data.ZMIN)/data.ZDIM))
        grid_z = []
        #keep track of maximal and minimal datavalue for contour-coloring
        minimum = 1000
        maximum = -1000
        #find temperature value z for every point in the grid, create a 2D-array in grid_z
        for x in range(data.XDIM):
            grid_z.append([])
            for y in range(data.YDIM):
                record = data.getRecord(x, y, z)
                #check whether record is new min/max
                if record < minimum:
                    minimum = record
                if record > maximum:
                    maximum = record
                grid_z[x].append(record)
            #make current grid row to np array for later plotting
            grid_z[x] = np.array(grid_z[x])
        #now generate the underlaying satelite map with the coordinates specified in the DataSet itself
        map = Basemap(projection='mill',
                    resolution="l", llcrnrlat=data.FROMLAT, llcrnrlon=data.FROMLON, urcrnrlat=data.TOLAT, urcrnrlon=data.TOLON)
        #set additional attributes like drawing of coastlines and states for better visibility or regions
        map.bluemarble()
        map.drawcoastlines()
        map.drawstates()
        map.drawcountries()
        #create an equally spaced meshgrid on top of the basemap
        X, Y = np.meshgrid(np.linspace(0, map.urcrnrx, data.XDIM), np.linspace(0, map.urcrnry, data.YDIM))
        #create a new colormap with 20 different entries, linearly spaced from minimal to maximal value in the dataset
        levels = np.arange(minimum, maximum, (maximum - minimum) / 20)
        #color the colormap newly and make it slightly transparent
        cmap = plt.cm.RdBu_r
        t_cmap = cmap(np.arange(cmap.N))
        t_cmap[:, -1] = np.linspace(2/3, 1, cmap.N)
        t_cmap = ListedColormap(t_cmap)
        #Create the contour plot
        mymap = ax.contourf(X, Y, grid_z, levels=levels, cmap=t_cmap)
        #create the colorbar
        plt.colorbar(mymap, ax=ax, orientation="vertical")
        #set some additional styling information like title and label
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_title('Contour Plot of Temperature at hour 1')
        ax.set_xlabel('latitude')
        ax.set_ylabel('longitude')


    #Crates a vectofield on top of a satelite map representing individual datavalues, the first two with vector direction and length, the second with colour
    @staticmethod
    def UVWPlot(windx, windy, windz, height, entries, ax):
        #create the underlaying satelite map again
        map = Basemap(projection='mill',
                      resolution="l", llcrnrlat=windx.FROMLAT, llcrnrlon=windx.FROMLON, urcrnrlat=windx.TOLAT, urcrnrlon=windx.TOLON)
        #add some additional arguments to satelite map like drawing coastlines for better visibility
        map.bluemarble()
        map.drawcoastlines()
        map.drawstates()
        map.drawcountries()
        #again, map equally spaced meshgrid over the satelite map
        X, Y = np.meshgrid(np.linspace(0, map.urcrnrx, entries), np.linspace(0, map.urcrnry, entries))
        #convert the given metric z-value to the data-set value
        z = round(height / ((windx.ZMAX + windx.ZMIN) / windx.ZDIM))
        data_z = []
        data_u = []
        data_v = []
        #pick entry * entry datapoints uniformly spaced and find the datavalue to data_z, data_u and data_v out of the first, second and third dataset
        for x in range(entries):
            for y in range(entries):
                data_u.append(x+windx.getRecord((windx.XDIM//entries)*x, (windx.YDIM//entries)*y, z))
                data_v.append(y+windy.getRecord((windy.XDIM//entries)*x, (windy.YDIM//entries)*y, z))
                data_z.append(windz.getRecord((windz.XDIM // entries) * x, (windz.YDIM // entries) * y, z))
        #map the vectorfield on top of the map into the meshgrid
        mymap = ax.quiver(X, Y, data_u, data_v, data_z, cmap=plt.cm.RdYlBu_r)
        #add the colourbar to the plot according to the data from the vectorfield
        plt.colorbar(mymap, ax=ax, orientation="vertical")
        #set some additional matplotlib styling arguments
        ax.set_title('UVW QuiverPlot')
        ax.set_xlabel('latitude')
        ax.set_ylabel('longitude')

    @staticmethod
    def matrixPlot(x, y, height, dataArray, names, axarr):
        #as usually, convert metric z value to dataset-z value
        z = round(height / ((dataArray[0].ZMAX + dataArray[0].ZMIN) / dataArray[0].ZDIM))
        dim = len(dataArray)
        #for every entry in matrix
        for x_direction in range(dim):
            for y_direction in range(dim):
                #find the corresonding values on x and y direction
                x_records = [dataArray[x_direction].getRecord(x[entry], y[entry], z) for entry in range(len(x))]
                y_records = [dataArray[y_direction].getRecord(x[entry], y[entry], z) for entry in range(len(x))]
                #now, we give some additional styling arguments to the outer ring like axis-description or title
                if y_direction == dim//2 and x_direction == 0:
                    axarr[x_direction][y_direction].set_title("Scaterplot Matrix")
                if x_direction == dim-1:
                    axarr[x_direction][y_direction].set_xlabel(names[y_direction])
                if y_direction == 0:
                    axarr[x_direction][y_direction].set_ylabel(names[x_direction])
                #for the special case that we deal with one of the diagonal-entries, we plot a histogram and continue
                if x_direction == y_direction:
                    axarr[x_direction][y_direction].hist(x_records)
                    continue
                #set the x and y axis a bit wider so that the most outer points are not cut in half
                #plot a scatterplot matrix into the current x-y matrix
                axarr[x_direction][y_direction].set_ylim(np.min(x_records)*1.1, np.max(x_records)*1.1)
                axarr[x_direction][y_direction].set_xlim(np.min(y_records)*1.1, np.max(y_records)*1.1)
                axarr[x_direction][y_direction].scatter(y_records, x_records, s=10)