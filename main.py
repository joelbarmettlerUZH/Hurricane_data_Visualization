import matplotlib.pyplot as plt
from matplotlib import style
import random
from DataSet import DataSet
from Plot import Plot

#defines a nicer looking for matplotlib
style.use("bmh")

#create new plt figure
figure = plt.figure()

#Scrape new DataSet containing temperature information at hour 1
temp = DataSet("temperature", 1)
#Create new ax plot on the top left of the subplot grid
ax1 = plt.subplot2grid((33,9),(0,0), rowspan=15, colspan=3)
#Create a heightplot at position of ax1
Plot.heightPlot(temp, 200, 250, ax1, title="Temperature at location (200,250)", xlabel="Height (m)", ylabel="Temperature (°C)")


#Define over how many hours the stacked plot shall be placed
anz_hours = 5
#create the first stacked plot which will be the leading one, all the others have its x-axis shared
ax2 = [plt.subplot2grid((33,9),(18,0), rowspan=3, colspan=3)]
#create all the other axis
for x in range(anz_hours-1):
    ax2.append(plt.subplot2grid((33,9),(21+(3*x),0), rowspan=3, colspan=3, sharex=ax2[x]))
#plot stacked plot on these axis
Plot.stackedPlot(anz_hours, 200, 250, ax2)


#Create again new axis
ax3 = plt.subplot2grid((33,9),(18,3), rowspan=15, colspan=3)
#Plot a countour plot on the axis, showing again the temp information at hour 1 on height 1000 meter
Plot.contourplotPlot(temp, ax3, 1000)


#Get wind datasets for each direction in 3D space
windx = DataSet("wind-x", 1)
windy = DataSet("wind-y", 1)
windz = DataSet("wind-z", 1)
#create again new figure at bottom right
ax4 = plt.subplot2grid((33,9),(18,6), rowspan=15, colspan=3)
#Plot UVW plot, so the plot with the vectorfield, on it
Plot.UVWPlot(windx, windy, windz, 1000, 22, ax4)



#get information about presure and wind for the scatterplot matrix
presure = DataSet("presure", 1)
wind = DataSet("wind-x", 1)
#define the entrie variables of the matrix
matrix = [temp, presure, wind]
#create n-squared many axis with n being the number of variables to present
ax5 = []
for i in range(len(matrix)):
    ax5.append([])
    for j in range(len(matrix)):
        ax5[i].append(plt.subplot2grid((33,9),(i*5,6+j), rowspan=5, colspan=1))
#collect sample_number many points at random and create scatterplot matrix with given axis
sample_number = 50
Plot.matrixPlot(random.sample(range(500), sample_number), random.sample(range(500), sample_number), height=1000, dataArray=matrix, names=("temperature", "presure", "wind-x"), axarr=ax5)


#Show the matplotlib plot
plt.show()












