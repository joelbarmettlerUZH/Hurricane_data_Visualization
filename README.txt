The Script was written with Python 3.6 using PyCharm and the following packages
-matplotlib.pyplot (pip install matplotlib)
-matplotlib.style (pip install matplotlib)
-random (standard)
-requests (pip install requests)
-gzip (standard)
-numpy (pip install numpy)
-os.path (standard)
-gdal (used by basemap, pip install GDAL, or for MAC brew install gdal [when having homebrew installed from brew.sh]) 
-pyproj (used by basemap, pip install pyproj)
-matplotlib.colors (pip install matplotlib)
-os.path (standard)
-mpl_toolkits.basemap (installation instruction found here: http://matplotlib.org/basemap/users/installing.html)


To execute the program, please run the main.py by opening the terminal, cd to the unzipped folder and calling
>>python main.py. All the necessarry files are downloaded, unzipped and opened automatically from the online 
website. The download process may take a few minutes, please do not interrupt.
If you want to download the files yourself, please just put them into the same directory as the main.py file
and the programm will recognize that the files are already on place, it therefore won't download them again.
Place either the .gz or the .bin file in the folder, both work fine. 
The link to the data files is: http://www.vets.ucar.edu/vg/isabeldata/

The Dashboard is quiet dense, so please make the opening matplotlib plot full-screen in order to enjoy
its beauty. I wanted to make it full-screen on default, but was not sure whether this would also work
for mac and linux, so I leave it up to you to make that click.

The needed packages are the following:
-TC01 (Temperature, Hour 1)
-TC02 (Temperature, Hour 2)
-TC03 (Temperature, Hour 3)
-TC04 (Temperature, Hour 4)
-TC05 (Temperature, Hour 5)
-U01  (Wind X direction, Hour 1)
-V01  (Wind Y direction, Hour 1)
-W01  (Wind Z direction, Hour 1)
-P01  (Presure, Hour 1)
