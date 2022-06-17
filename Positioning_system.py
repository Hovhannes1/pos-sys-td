# # TD1
# ## RSSI sample
from __future__ import annotations
import numpy as np
import csv
import math


class RSSISample:
    # constroctor and only leaving two floating numbers in rssi
    def __init__(self, mac_address: str, rssi: float) -> None:
        self.mac_address = mac_address
        self.rssi = math.floor(rssi*100)/100
    # printing function

    def printing(self):
        strin = str(self.mac_address)+","+str(self.rssi)
        return strin


# ## Fingerprint sample


class FingerprintSample:
    # initilize
    def __init__(self, samples: list[RSSISample]) -> None:
        self.samples = samples

    # printing function
    def printing(self):
        strin = ""
        for l in self.samples:
            strin = strin+","+l.printing()
        return strin


# ## Location

class SimpleLocation:
    # initilize
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    # defining funtion to be able to compare two objects
    def __eq__(self, pos):
        return self.x == pos.x and self.y == pos.y and self.z == pos.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __ne__(self, other):
        return not(self == other)

    # printing function

    def printing(self):
        strin = str(self.x)+","+str(self.y)+","+str(self.z)
        return strin


# ## Fingerprint

class Fingerprint:

    # initilize
    def __init__(self, position: SimpleLocation, sample: FingerprintSample) -> None:
        self.position = position
        self.sample = sample

    # printing function
    def printing(self):
        print(str(self.position.printing())+",0"+str(self.sample.printing()))


# ## Fingerprint database


class FingerprintDatabase:

    # initilize
    def __init__(self) -> None:
        # the db where i read from csv in will be a dictionary
        self.db = {}
        # the result list will be saved in here, it is a list of fingerprints
        self.res = []

    # this function will read from csv, it pretty complex because it will read into a
    # dictionary and check for mac and position duplications
    def readingCSVdata(self):
        with open('data.csv', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        for i in range(len(data)):
            pos = SimpleLocation(float(data[i][0]), float(
                data[i][1]), float(data[i][2]))
            if(not(pos in self.db.keys())):
                j = 4
                address = {}
                while(j < len(data[i])):
                    if(data[i][j] in address.keys()):
                        address[data[i][j]].append(data[i][j+1])
                    else:
                        lis = [data[i][j+1]]
                        address.update({data[i][j]: lis})
                    j = j+2
                self.db.update({pos: address})
            else:
                j = 4
                while(j < len(data[i])):
                    if(data[i][j] in self.db[pos].values()):
                        self.db[pos][data[i][j]].append(data[i][j+1])
                    else:
                        lis = [data[i][j+1]]
                        self.db[pos].update({data[i][j]: lis})
                    j = j+2
                self.db.update({pos: address})

    # this function is responsible for the average calculations
    def rssiValcheck(self):
        for i in self.db.values():
            for x in i:
                try:
                    lis = i[x]
                    if len(lis) > 1:
                        somme = 0
                        for j in lis:
                            somme = somme + 10**(float(j) / 10.)
                        avg = somme/len(lis)
                        val = 10. * math.log10(avg)
                        i.update({x: val})
                    else:
                        i.update({x: float(lis[0])})
                except:
                    pass

     # this function is the one responsible for switching from dictionary db to res list
    def resultarray(self):
        for x in self.db:
            y = self.db[x]
            rssisamp = []
            for i in y:
                rssisamp.append(RSSISample(i, y[i]))
            fin = FingerprintSample(rssisamp)
            self.res.append(Fingerprint(x, fin))

    # this function is the one responsible for checking None objects and deleting them from list and same time printing
    def printing(self):
        for r in self.res:
            if(r.printing() == None):
                self.res.remove(r)
            else:
                print(r.printing())

# Now let check the result in our main file


hi = FingerprintDatabase()
hi.readingCSVdata()
hi.rssiValcheck()
hi.resultarray()
hi.printing()


# # ------------------------------------------------------------------------------------------------------------


# # TD2
# ## Access Points data

class AccessPoint:
    def __init__(self, mac: str, loc: SimpleLocation,  f: float, a: float, p: float):
        self.mac_address = mac
        self.location = loc
        self.output_power_dbm = p
        self.antenna_dbi = a
        self.output_frequency_hz = f

    def distanceTo(self, point):
        return math.sqrt((point[0] - self.location.x) ** 2 + (point[1] - self.location.y) ** 2 + (point[2] - self.location.z) ** 2)


AP = {"00:13:ce:95:e1:6f": AccessPoint("00:13:ce:95:e1:6f", SimpleLocation(4.93, 25.81, 3.55), 2417000000, 5.0, 20.0),
      "00:13:ce:95:de:7e": AccessPoint("00:13:ce:95:de:7e", SimpleLocation(4.83, 10.88, 3.78), 2417000000, 5.0, 20.0),
      "00:13:ce:97:78:79": AccessPoint("00:13:ce:97:78:79", SimpleLocation(20.05, 28.31, 3.74), 2417000000, 5.0, 20.0),
      "00:13:ce:8f:77:43": AccessPoint("00:13:ce:8f:77:43", SimpleLocation(4.13, 7.085, 0.80), 2417000000, 5.0, 20.0),
      "00:13:ce:8f:78:d9": AccessPoint("00:13:ce:8f:78:d9", SimpleLocation(2.74, 0.35, 1.04), 2417000000, 5.0, 20.0)}


def compute_FBCM_index(distance: float, rssi_values: RSSISample, ap: AccessPoint) -> float:
    wavelen = 3e8 / ap.output_frequency_hz
    wavelenlog = 20 * math.log10(wavelen / 4 * math.pi)
    formula = (ap.output_power_dbm - rssi_values.rssi +
               ap.antenna_dbi + 2.1 + wavelenlog)/(10 * math.log10(distance))
    return formula


def estimate_distance(rssi_avg: float, fbcm_index: float, ap: AccessPoint) -> float:
    wavelen = 3e8 / ap.output_frequency_hz
    pr = (ap.output_power_dbm - rssi_avg + ap.antenna_dbi + 2.1 + 20 *
          math.log10(wavelen) - 20*math.log10(4*math.pi))/(10.0 * fbcm_index)
    distance = pow(10, pr)
    return distance


def multilateration(distances: dict[str, float], ap_locations: dict[str, SimpleLocation]) -> SimpleLocation:
    xMin = 99
    xMax = 0
    yMin = 99
    yMax = 0
    zMin = 99
    zMax = 0
    dMin = 99

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

        step = 0.1

    for x in np.arange(xMin, xMax, step):
        for y in np.arange(yMin, yMax, step):
            for z in np.arange(zMin, zMax, step):
                location = SimpleLocation(
                    round(x, 4), round(y, 4), round(z, 4))
                distance = 0
                for j in distances:
                    distance = distance + math.sqrt(math.pow(ap_locations[j].location.x - location.x, 2) + math.pow(
                        ap_locations[j].location.y - location.y, 2) + math.pow(ap_locations[j].location.z - location.z, 2))
                if distance < dMin:
                    dMin = distance
                    min_location = location
    return min_location


dist = round(estimate_distance(-57.0, 3.5, AP["00:13:ce:95:e1:6f"]), 3)
print(dist)
rs = RSSISample("00:13:ce:95:e1:6f", -100.0)
i = round(compute_FBCM_index(dist, rs, AP["00:13:ce:95:e1:6f"]), 3)
print(i)
dist = round(estimate_distance(
    rs.rssi, round(i, 3), AP["00:13:ce:95:e1:6f"]), 3)
print(dist)
multi = multilateration({"00:13:ce:97:78:79": 1, "00:13:ce:95:de:7e": 10,
                        "00:13:ce:8f:78:d9": 50, "00:13:ce:95:e1:6f": 5, "00:13:ce:8f:77:43": 3}, AP)
print(multi.printing())


# # ------------------------------------------------------------------------------------------------------------


# # TD3
# ## Simple matching


def rssi_distance(sample1: dict[str, float], sample2: dict[str, float]) -> float:
    somme = []
    for i in sample2:
        somme.append(abs(abs(sample1[i])-abs(sample2[i])))
    return sum(somme)


def simple_matching(db: FingerprintDatabase, sample: dict[str, float]) -> SimpleLocation:
    mindist = 1000
    pos = 0
    for i in db.db:
        dist = rssi_distance(sample, db.db[i])
        if(dist < mindist):
            mindist = dist
            pos = i
    return pos


pos = simple_matching(hi, {"00:13:ce:95:de:7e": -38.0, "00:13:ce:95:e1:6f": -54.0,
                      "00:13:ce:8f:78:d9": -64.0, "00:13:ce:8f:77:43": -68.0, "00:13:ce:97:78:79": -80.0})
print(pos.printing())
# 5.4,6.48,4.2,0,00:13:ce:95:de:7e,-38.0,00:13:ce:95:e1:6f,-54.0,00:13:ce:8f:78:d9,-64.0,00:13:ce:8f:77:43,-68.0,00:13:ce:97:78:79,-80.0

# ## Histogram matching


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


def probability(histo1: NormHisto, histo2: NormHisto) -> float:
    # compute the probability of two histograms
    # :param histo1: the first histogram
    # :param histo2: the second histogram
    return sum([histo1.get_normalized_histogram()[i] * histo2.get_normalized_histogram()[i] for i in histo1.get_normalized_histogram()])


def histogram_matching(db: FingerprintDatabase, sample: NormHisto) -> SimpleLocation:
    # compute a location based on a histogram sample
    # :param db: the fingerprint database
    # :param sample: the histogram sample
    # :return: a SimpleLocation
    min_prob = 9999
    min_location = SimpleLocation(0, 0, 0)
    lis = {}
    for i in db.db:
        c = 0
        for n in db.db[i]:
            lis.update(c, db.db[i][n])
            c += 1
        histo = NormHisto(lis)
        prob = probability(sample, histo)
        if prob < min_prob:
            min_prob = prob
            min_location = i
    return min_location


data = {1: -38.0, 0: -54.0, 30: -64.0, 10: -68.0, 5: -80.0}
da = NormHisto(data)
pos = histogram_matching(hi, da)
pos.printing()


# ## Gauss matching

class GaussModel:
    def _init_(self, avg: float, stddev: float):
        self.average_rssi = avg
        self.standard_deviation = stddev
        self.gaussian_function = {}
        self.compute_gaussian_function()

    def compute_gaussian_function(self):
        # compute the gaussian function
        for i in range(-100, 101):
            self.gaussian_function[i] = math.exp(-((i - self.average_rssi) * 2) / (
                2 * self.standard_deviation * 2)) / (math.sqrt(2 * math.pi) * self.standard_deviation)

    def get_gaussian_function(self):
        return self.gaussian_function

    def get_average_rssi(self):
        return self.average_rssi

    def get_standard_deviation(self):
        return self.standard_deviation

    def normal(self, x):
        return (1 / (math.sqrt(2 * math.pi) * self.standard_deviation)) * math.exp(- (1/2) * ((x - self.average_rssi)/self.standard_deviation)**2)


def histogram_from_gauss(sample: GaussModel) -> NormHisto:
    # compute a histogram sample from a Gaussian model
    # :param sample: the Gaussian model
    # :return: a histograme

    histo = {}
    L = [i for i in range(math.floor(sample.average_rssi)-10,
                          math.floor(sample.average_rssi)+10)]
    for dbm in L:
        histo[dbm] = sample.normal(dbm)
    return NormHisto(histo)


def variance(data, ddof=0):
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - ddof)


def stdev(data):
    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev


def Average(lst):
    return sum(lst) / len(lst)


dat = [-38.0, -54.0, -64.0, -68.0, -80.0]
st = stdev(data)
data = GaussModel(Average(data), st)
da = NormHisto(data)
pos = histogram_matching(hi, da)
pos.printing()
