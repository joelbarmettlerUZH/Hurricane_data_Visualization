import requests
import gzip
import numpy as np
import os.path
import shutil

class DataSet(object):
    def __init__(self, category="temperature", timestep=1):
        self._category = category
        self._timestep = timestep
        # defined values for a data record
        self.XDIM = 500
        self.YDIM = 500
        self.ZDIM = 100
        self.TDIM = 1
        self.ZMIN = 35
        self.ZMAX = 19835
        self.FROMLAT = 23.7
        self.TOLAT = 41.7
        self.FROMLON = -83
        self.TOLON = -62
        self.__data = self.getPackage(timestep, category)

    #downloads a certain package, unzips it and returns the data as a numpy array
    def getPackage(self, packagenumber, variable):
        #convert names to the pseudonames used online
        code = {
            "moisture": "QCLOUD",
            "graupel": "QGRAUP",
            "ice": "QICE",
            "snow": "QSNOW",
            "vapor": "QVAPOR",
            "cloud": "CLOUD",
            "precipitation": "PRECIP",
            "presure": "P",
            "temperature": "TC",
            "wind-x": "U",
            "wind-y": "V",
            "wind-z": "W"
        }
        var = code[variable]
        #bring the package number into the form "0X" when it is only one digit large
        if packagenumber < 10:
            number = "0"+str(packagenumber)
        else:
            number = str(packagenumber)
        #if unzipped file already exists, rename it accordingly
        if os.path.isfile(var + "f" + number + ".bin"):
            os.rename(var + "f" + number + ".bin", variable + number + ".bin")
        #unzipp the file and return its content as numpy array
        if os.path.isfile(variable + number + ".bin"):
            print("-File already downloaded and unzipped, skipping.")
            return np.fromfile(variable + number + ".bin", dtype='>f')
        #If package .gz already exists but with old / original name, rename it
        if os.path.isfile(var+"f"+number+".bin.gz"):
            os.rename(var+"f"+number+".bin.gz", variable+number+".bin.gz")
        #if package .gz exists with, check whether it has the needed file size. This is not the case when a download was interrupted or a file is corrupted
        if os.path.isfile(variable + number + ".bin.gz") and (os.path.getsize(variable + number + ".bin.gz")
                          != int(requests.head("http://www.vets.ucar.edu/vg/isabeldata/"+var+"f"+number+".bin.gz",headers={'Accept-Encoding': 'identity'}).headers['content-length'])):
            print("-Similar file exists, but seems to be corrupted. Downloading it again to be sure to have valid data")
            #remove the file when it is corrupted so it will be downloaded again
            os.remove(variable + number + ".bin.gz")
        #if the .gz file still exists untill now, unzip it and do not download it again
        if os.path.isfile(variable+number+".bin.gz"):
            print("-File already downloaded, skipping.")
            return self.unzip(variable + number + ".bin.gz")
        #get the bin.gz file from ucar.edu via request cause it does not exist yet
        print("-Downlaoding " + var + number+". This may take a few minutes")
        #Try to establish a download connection
        try:
            request = requests.get("http://www.vets.ucar.edu/vg/isabeldata/"+var+"f"+number+".bin.gz", stream=True)
        except:
             print("File could not be downloaded. Please download file manually and place in folder, then restart the software. \nHere ist the link: http://www.vets.ucar.edu/vg/isabeldata/"+var+"f"+number+".bin.gz")
             exit()
        print("-Saving File to Disk")
        #save the request content to a file on the local disk
        with open(variable+number+".bin.gz", "wb") as file:
            shutil.copyfileobj(request.raw, file)
        #unzip file and return the unzipped values
        return self.unzip(variable+number+".bin.gz")

    #unzips a .gz file and returns its content
    def unzip(self, name):
        new_filename = name.replace(".gz","")
        #only unzip file when it is not already unzipped
        if os.path.isfile(new_filename):
            print("-File already unzipped, skipping.")
        else:
            print("-Unzipping file")
            #open file as gzip file
            with gzip.open(name, "rb") as readfile:
                #rad content and save it back to the disk
                fileContent = readfile.read()
                with open(new_filename, "wb") as writefile:
                    writefile.write(fileContent)
        #open unzipped file and return its content as np array
        return np.fromfile(new_filename, dtype='>f')

    #returns a datarecord for x,y,z and t values
    def getRecord(self, x, y, z, t=1, treshold=1000000):
        #find the datarecord in the datalist
        record = self.__data[x + self.XDIM * (y + self.YDIM * z)]
        #if the size of the record is above or below a certain threshold, we suspect it to be an outlier and take its neighbour as a reference then.
        if abs(record) < treshold:
            return self.__data[x + self.XDIM * (y + self.YDIM * z)]
        #return the datapoint directly if the size is in the threshold range
        return self.getRecord(x+1, y, z, t, treshold)