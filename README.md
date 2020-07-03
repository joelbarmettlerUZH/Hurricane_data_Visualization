# Hurricane Data Visualization - [Computer.org](http://vis.computer.org/vis2004contest/data.html) Contest of the year 2004

This implementation of the Computer.org Contest of the year 2004 visualizes complex Hurricane data from real-world datasets. A Matplotlib dashboard is created showing data about the temperature drop with increasing height at a specific point in the hurricane *(Plot 1)*, as well as the same temperature graph at five different locations for comparison *(Plot 2)*. Further, the Plot contains a Contour Plot visualizing the Temperature at the first hour of the Hurricane after data recording begun at a height of 1000 meters *(Plot 3)*. A Vectorfield-Plot visualizes the wind speed and direction in the whole recorded area, again at the height of 1000 meters *(Plot 4)*. Last, a Scatterplot Matrix shows the correlation between Windspeed in X-Direction, Presure and temperature *(Plot 5)*.

![Dashboard](https://github.com/joelbarmettlerUZH/Hurricane_data_Visualization/raw/master/dashboard.png)

# Overview
While creating this script, the focus lied on the following properties:

  - Automatically download all needed files from the [computer.org](http://www.vets.ucar.edu/vg/isabeldata/) website
  - Seperate Plot-Creation and Dashboard strictly
  - Make visualized Data per Plot ineerchangable by providing another Dataset


## Usage
In the following paragraphs, I am going to describe how you can get and use the the Python Scripts for your own projects.

###  Getting it
The Script was written with Python 3.6 using PyCharm and the following packages
- matplotlib.pyplot *(pip install matplotlib)*
- matplotlib.style *(pip install matplotlib)*
- random
- requests *(pip install requests)*
- gzip 
- numpy *(pip install numpy)*
- os.path
- gdal *(used by basemap, pip install GDAL, or for MAC brew install gdal [when having homebrew installed from brew.sh])*
- pyproj *(used by basemap, pip install pyproj)*
- matplotlib.colors *(pip install matplotlib)*
- os.path
- mpl_toolkits.basemap *(installation instruction found [here](http://matplotlib.org/basemap/users/installing.html) )*

To get the source code, Fork the github repo to your local disk and place the .py classes into your project directory.
[You find the Source code here](https://github.com/joelbarmettlerUZH/Hurricane_data_Visualization)

### Creating a Matplitlib Dashboard

First, import all libraries that are needed to create a matplotlib grid, a dataset and a Plot

```python
import matplotlib.pyplot as plt
from matplotlib import style
from DataSet import DataSet
from Plot import Plot
```

Note that DataSet and Plot are Python files provided in this Github Repo. *Plot* contains a bunch of static methods to insert new matplotlib plots into Subplots. Dataset is the data-downloader that allows you to not just easily download the data you need with one Command, but also loads the data into the provided variable for direct usage. 

```python
temp = DataSet("temperature", 1)
```

To create a new Matplotlib dashboard, define the matplotlib style and create a new figure. 

```python
style.use("bmh")
figure = plt.figure()
```

Then, for each plot, create a new sublotgrid and name the total grid size *(X, Y)* as well as the position of the upper right corner *(x,y)* and the size of the plot *(rowspan=x, cospan=y)*. Save the subplotgrid into a variable and pass it into the *Plot.somePlot()* method in order to insert a new Plot into that subplot.

```python
ax1 = plt.subplot2grid((33,9),(0,0), rowspan=15, colspan=3)
Plot.someplot(ax1, temp)
```

Repeat that process for every Plot you want to create. Finally, as a last statement, call Plot.show():

```python
plt.show()
```

Note that the Dashboard provided in the Main.py script has a dimension of (X,Y) = (33, 9), where every Plot in y-Dimension has a size of x=15 and y=3 normally, so one third of each axis *(plus some space in between for the x-axis that is needed when displaying the quite dense scatterplot-matrix)*. 

### Creating a Temperature line
The first Plot is a simple Temperature plot that shows the Temperature at the Position **200, 250** at the hour **1** after data recording began. First, we create a new Dataset containing the temperature at hour 1. Then, we create a new empty subplotgrid and finally call heightPlot with our parameters.

```python
temp = DataSet("temperature", 1)
ax1 = plt.subplot2grid((33,9),(0,0), rowspan=15, colspan=3)
Plot.heightPlot(temp, 200, 250, ax1, title="Temperature at location (200,250)", xlabel="Height (m)", ylabel="Temperature (°C)")
```

### Creating stacked Temperature lines
While stacking the creational procedure is similar to just creating a normal Temperature line, we now need to loop over some specific number of hours (here we deal with 5 hours resulting in 5 plots) and create a new list of Subplotgrids called ax2 which we then use for calling Plot.stackedPlot. 

```python
anz_hours = 5
ax2 = [plt.subplot2grid((33,9),(18,0), rowspan=3, colspan=3)]
for x in range(anz_hours-1):
    ax2.append(plt.subplot2grid((33,9),(21+(3*x),0), rowspan=3, colspan=3, sharex=ax2[x]))
Plot.stackedPlot(anz_hours, 200, 250, ax2)
```

### Creating a Contour Plot
Since we already have our temperature dataset, we simply call Plot.contourPlot with a new subplotgrid and the height of 1000 Meters. 

```python
ax3 = plt.subplot2grid((33,9),(18,3), rowspan=15, colspan=3)
Plot.contourplotPlot(temp, ax3, 1000)
```

### Creating a Vectorfield Plot
Our Vectorfield shall display wind direction and strength in 3 dimensions, so we need three datasets for each direction. Then, we introduce yet another subplot and call Plot.UVWPlot with our different wind datasets, the height of 1000 meters and a number of vectors we want to display in each direction. 

```python
windx = DataSet("wind-x", 1)
windy = DataSet("wind-y", 1)
windz = DataSet("wind-z", 1)
ax4 = plt.subplot2grid((33,9),(18,6), rowspan=15, colspan=3)
Plot.UVWPlot(windx, windy, windz, 1000, 22, ax4)
```

### Creating a Scatterplot Matrix
We show relations between three different Datasets in our Scatterplot Matrix, we therefore need three datasets and create a one dimensional matrix in form of a list out of them. Then, we create 3*3 different subplotgrids and pass the datamatrix together with the subplots as parameters into Plot.matrixPlot, with specifiying the location of the sample-point (here it is randomized to pick one in the whole field), as well as the chosen height of 1000 Meters.

```python
presure = DataSet("presure", 1)
wind = DataSet("wind-x", 1)
matrix = [temp, presure, wind]
ax5 = []
for i in range(len(matrix)):
    ax5.append([])
    for j in range(len(matrix)):
        ax5[i].append(plt.subplot2grid((33,9),(i*5,6+j), rowspan=5, colspan=1))
sample_number = 50
Plot.matrixPlot(random.sample(range(500), sample_number), random.sample(range(500), sample_number), height=1000, dataArray=matrix, names=("temperature", "presure", "wind-x"), axarr=ax5)
```

## Quick run
To execute the program, please run the [main.py](https://github.com/joelbarmettlerUZH/Hurricane_data_Visualization/blob/master/main.py) by opening the terminal, cd to the unzipped folder and calling
python [main.py](https://github.com/joelbarmettlerUZH/Hurricane_data_Visualization/blob/master/main.py). All the necessarry files are downloaded, unzipped and opened automatically from the online 
website. The download process may take a few minutes, please do not interrupt.
If you want to download the files yourself, please just put them into the same directory as the [main.py](https://github.com/joelbarmettlerUZH/Hurricane_data_Visualization/blob/master/main.py) file
and the programm will recognize that the files are already on place, it therefore won't download them again.
Place either the .gz or the .bin file in the folder, both work fine. 
The link to the data files is [here](http://www.vets.ucar.edu/vg/isabeldata/)!

The Dashboard is quiet dense, so please make the opening matplotlib plot full-screen in order to enjoy
its beauty. I wanted to make it full-screen on default, but was not sure whether this would also work
for mac and linux, so I leave it up to you to make that click.

##### The needed packages are the following:
- TC01 (Temperature, Hour 1)
- TC02 (Temperature, Hour 2)
- TC03 (Temperature, Hour 3)
- TC04 (Temperature, Hour 4)
- TC05 (Temperature, Hour 5)
- U01  (Wind X direction, Hour 1)
- V01  (Wind Y direction, Hour 1)
- W01  (Wind Z direction, Hour 1)
- P01  (Presure, Hour 1)


License
----

MIT License

Copyright (c) 2018 Joel Barmettler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



Hire us: [Software Entwickler in Zürich](https://polygon-software.ch)!
