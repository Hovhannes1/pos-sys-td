from __future__ import annotations
import numpy as np
import math

# %% [markdown]
# ## RSSI sample

# %%

class RSSISample:
    def __init__(self, mac_address: str, rssi: float) -> None:
        self.mac_address = mac_address
        self.rssi = math.floor(rssi*100)/100 
    def printing(self):
        strin= str(self.mac_address)+", "+str(self.rssi)
        return strin

# %% [markdown]
# ## Fingerprint sample
# 

# %%
from math import log10
class FingerprintSample:
    #initilize
    def __init__(self, samples: RSSISample) -> None:
        self.samples = samples
    def printing(self):
        strin=""
        for l in self.samples:
            strin=strin+","+l.printing()
        return strin

# %% [markdown]
# ## Location

# %%
class SimpleLocation:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
    def __eq__(self, pos):
        return self.x==pos.x and self.y==pos.y and self.z==pos.z
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    def __ne__(self, other):
        return not(self == other)
    def printing(self):
        strin=str(self.x)+","+str(self.y)+","+str(self.z)
        return strin

# %% [markdown]
# ## Fingerprint

# %%
class Fingerprint:
    def __init__(self, position: SimpleLocation, sample: FingerprintSample) -> None:
        self.position = position
        self.sample = sample
    def printing(self):
        print(str(self.position.printing())+",0"+str(self.sample.printing()))

# %% [markdown]
# ## Fingerprint database
# 

# %%
import csv
import math
from math import log10

class FingerprintDatabase:
    def __init__(self) -> None:
        self.db = {}
        self.res=[]
    def readingCSVdata(self):
        with open('data.csv', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        for i in range(len(data)): 
            pos= SimpleLocation(float(data[i][0]),float(data[i][1]),float(data[i][2]))
            if(not(pos in self.db.keys())):
                j=4
                address={}
                while(j<len(data[i])):
                    if(data[i][j] in address.keys()):
                        address[data[i][j]].append(data[i][j+1])
                    else:
                        lis =[data[i][j+1]]
                        address.update({data[i][j]: lis})
                    j=j+2
                self.db.update({pos: address})
            else:
                j=4
                while(j<len(data[i])):
                    if(data[i][j] in self.db[pos].values()):
                        self.db[pos][data[i][j]].append(data[i][j+1])
                    else:
                        lis =[data[i][j+1]]
                        self.db[pos].update({data[i][j]: lis})
                    j=j+2
                self.db.update({pos: address})
    def rssiValcheck(self):
        for i in self.db.values():
            for x in i :
                try:
                    lis=i[x] 
                    if len(lis)>1:
                        somme = 0
                        for j in lis:
                            somme=somme + 10**(float(j)/ 10.)                        
                        avg=somme/len(lis)
                        val= 10. * math.log10(avg)
                        i.update({x: val})
                    else: 
                        i.update({x: float(lis[0])})      
                except:
                    pass
                               
    def outputingResult(self):
        for r in self.res:
            if(r.printing() == None):
                self.res.remove(r)
            else:
                print(r.printing())     
    def appendResult(self):
        for x in self.db:
            y=self.db[x]
            rssisamp=[]
            for i in y:
                rssisamp.append(RSSISample(i,y[i]))
            fin=FingerprintSample(rssisamp)
            self.res.append(Fingerprint(x,fin))
            

# %%
TD1 = FingerprintDatabase()
TD1.readingCSVdata()
TD1.rssiValcheck()
TD1.appendResult()
TD1.outputingResult()

# %% [markdown]
# # TD 2

# %% [markdown]
# ## Access Points data
# 

# %%
# Add an AccessPoint class with the desired members to build and access AP data. The class is based on the following fields:
class AccessPoint:
    def __init__(self, mac: str, loc: SimpleLocation, f: float, a: float, p: float):
        self.mac_address = mac
        self.location = loc
        self.output_power_dbm = p
        self.antenna_dbi = a
        self.output_frequency_hz = f
    # acces the AP data test_data.csv
    # def readingCSVdata(self):
    #     with open('test_data.csv', newline='') as f:
    #         reader = csv.reader(f)
    #         data = list(reader)
    #     for i in range(len(data)): 
    #         if(data[i][0]==self.mac_address):
    #             self.output_power_dbm=float(data[i][1])
    #             self.antenna_dbi=float(data[i][2])
    #             self.output_frequency_hz=float(data[i][3])
    # def printing(self):
    #     string=str(self.mac_address)+","+str(self.location.printing())+","+str(self.output_power_dbm)+","+str(self.antenna_dbi)+","+str(self.output_frequency_hz)
    #     return string
    
        

# %%
AP = {"00:13:ce:95:e1:6f": AccessPoint("00:13:ce:95:e1:6f", SimpleLocation(4.93, 25.81, 3.55), 2417000000, 5.0, 20.0),
      "00:13:ce:95:de:7e": AccessPoint("00:13:ce:95:de:7e", SimpleLocation(4.83, 10.88, 3.78), 2417000000, 5.0, 20.0), 
      "00:13:ce:97:78:79": AccessPoint("00:13:ce:97:78:79", SimpleLocation(20.05, 28.31, 3.74), 2417000000, 5.0, 20.0), 
      "00:13:ce:8f:77:43": AccessPoint("00:13:ce:8f:77:43", SimpleLocation(4.13, 7.085, 0.80), 2417000000, 5.0, 20.0), 
      "00:13:ce:8f:78:d9": AccessPoint("00:13:ce:8f:78:d9", SimpleLocation(5.74, 30.35, 2.04), 2417000000, 5.0, 20.0)}

# %%

def compute_FBCM_index(distance: float, rssi_values: RSSISample, ap: AccessPoint) -> float:
    # compute a FBCM index based on the distance (between transmitter and receiver)
    # and the AP parameters. We consider the mobile device's antenna gain is 2.1 dBi.
    # :param distance: the distance between AP and device
    # :param rssi_values: the RSSI values associated to the AP for current calibration point. Use their average value.
    # :return: one value for the FBCM index
    wavelen= 3e8 / ap.output_frequency_hz
    wavelenlog=20 * math.log10(wavelen/ 4 * math.pi)
    return ( ap.output_power_dbm - rssi_values.rssi + ap.antenna_dbi + 2.1 + wavelenlog)/(10 * math.log10(distance))

def estimate_distance(rssi_avg: float, fbcm_index: float, ap: AccessPoint) -> float:
    # estimate the distance between an access point and a test point based on the test point rssi sample.
    # :param rssi: average RSSI value for test point
    # :param fbcm_index: index to use
    # :param ap: access points parameters used in FBCM
    # :return: the distance (meters)
    wavelen= 3e8 / ap.output_frequency_hz
    pr= ( ap.output_power_dbm - rssi_avg + ap.antenna_dbi + 2.1 + 20*math.log10(wavelen) - 20*math.log10(4*math.pi))/(10.0 * fbcm_index)
    distance =pow(10,pr)
    return distance

def multilateration(distances: dict[str, float], ap_locations: dict[str, SimpleLocation]) -> SimpleLocation:
    # With distances between a device and at least 3 references, compute device's location. You may use grid search
    # :param distances: the distances associated to the related AP MAC addresses as a string
    # :param ap_locations: the access points locations, indexed by AP MAC address as strings
    # :return: a location
    xMin = 9999
    xMax = 0
    yMin = 9999
    yMax = 0
    zMin = 9999
    zMax = 0
    dMin = 9999

    for i in distances:
        c_xMin = ap_locations[i].location.x - distances[i]
        c_xMax = ap_locations[i].location.x + distances[i]
        c_yMin = ap_locations[i].location.y - distances[i]
        c_yMax = ap_locations[i].location.y + distances[i]
        c_zMin = ap_locations[i].location.z - distances[i]
        c_zMax = ap_locations[i].location.z + distances[i]
        if c_xMin < xMin:
            xMin = c_xMin
        if c_xMax > xMax:
            xMax = c_xMax
        if c_yMin < yMin:
            yMin = c_yMin
        if c_yMax > yMax:
            yMax = c_yMax
        if c_zMin < zMin:
            zMin = c_zMin
        if c_zMax > zMax:
            zMax = c_zMax

        step = 0.5

    for x in np.arange(xMin, xMax, step):
        for y in np.arange(yMin, yMax, step):
            for z in np.arange(zMin, zMax, step):
                location = SimpleLocation(round(x,2), round(y,2), round(z,2))
                distance = 0
                for j in distances:
                    distance += math.sqrt(math.pow(ap_locations[j].location.x - location.x, 2) + math.pow(ap_locations[j].location.y - location.y, 2) + math.pow(ap_locations[j].location.z - location.z, 2))
                if distance < dMin:
                    dMin = distance
                    min_location = location
    return min_location
    

# %%
# Use all functions to provide compute locations for the test data set provided with these instructions (calibration data will be TD1 data)
dis = estimate_distance(-70.0, 3.5, AP["00:13:ce:95:e1:6f"])
print(dis)
# compute_FBCM_index
rs = RSSISample("00:13:ce:95:e1:6f", -54.0)
fbcm = compute_FBCM_index(dis, rs, AP["00:13:ce:95:e1:6f"])
print(fbcm)
# estimate_distance
dis = estimate_distance(rs.rssi, fbcm, AP["00:13:ce:95:e1:6f"])

print(dis)

multi = multilateration({"00:13:ce:95:e1:6f":6 ,"00:13:ce:97:78:79":8 ,"00:13:ce:8f:78:d9":5},AP)
print(multi.printing())


# %% [markdown]
# # TD 3

# %% [markdown]
# ## Simple matching

# %%
#something
def rssi_distance(sample1: dict[str, float], sample2: dict[str, float]) -> float:
	# compute the distance between two RSSI samples
	# :param sample1: the first RSSI sample
	# :param sample2: the second RSSI sample
	return math.sqrt((sample1["rssi"] - sample2["rssi"]) ** 2)

def simple_matching(db: FingerprintDatabase, sample: dict[str, float]) -> SimpleLocation:
	# compute a location based on a RSSI sample
	# :param db: the fingerprint database
	# :param sample: the RSSI sample
	return db.match(sample)

# %% [markdown]
# ## Histogram matching
# 

# %%
class NormHisto:
	def __init__(self, histo: dict[int, float]):
		self.histogram = histo
		self.normalized_histogram = {}
		self.normalize()
	def normalize(self):
		# normalize the histogram
		sum_histo = 0
		for i in self.histogram:
			sum_histo += self.histogram[i]
		for i in self.histogram:
			self.normalized_histogram[i] = self.histogram[i] / sum_histo
	def get_normalized_histogram(self):
		return self.normalized_histogram
	def get_histogram(self):
		return self.histogram
	
    

# %%
def probability(histo1: NormHisto, histo2: NormHisto) -> float:
	# compute the probability of two histograms
	# :param histo1: the first histogram
	# :param histo2: the second histogram
	return sum([histo1.get_normalized_histogram()[i] * histo2.get_normalized_histogram()[i] for i in histo1.get_normalized_histogram()])

def histogram_matching(db: FingerprintDatabase, sample: NormHisto) -> SimpleLocation:
	# compute a location based on a histogram sample
	# :param db: the fingerprint database
	# :param sample: the histogram sample
	return db.match(sample)

# %% [markdown]
# ## Gauss matching
# 

# %%
class GaussModel:
	def __init__(self, avg: float, stddev: float):
		self.average_rssi = avg
		self.standard_deviation = stddev
		self.gaussian_function = {}
		self.compute_gaussian_function()
	def compute_gaussian_function(self):
		# compute the gaussian function
		for i in range(-100, 101):
			self.gaussian_function[i] = math.exp(-((i - self.average_rssi) ** 2) / (2 * self.standard_deviation ** 2)) / (math.sqrt(2 * math.pi) * self.standard_deviation)
	def get_gaussian_function(self):
		return self.gaussian_function
	def get_average_rssi(self):
		return self.average_rssi
	def get_standard_deviation(self):
		return self.standard_deviation
		

# %%
def histogram_from_gauss(sample: GaussModel) -> RSSISample:
	# compute a histogram sample from a Gaussian model
	# :param sample: the Gaussian model
	return RSSISample(sample.get_average_rssi(), sample.get_gaussian_function())

# %% [markdown]
# ## Lab
# 

# %%
# from flask import Flask
# app = Flask(__name__)




