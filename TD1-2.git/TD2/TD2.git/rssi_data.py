from math import log10, sqrt
from enum import Enum
import csv


class Location:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other):
        return sqrt((self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)**2)


class Orientation(Enum):
    UNDEFINED = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

    def __cmp__(self, other):
        if self.value < other.value:
            return -1
        if self.value > other.value:
            return 1
        return 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0


class OrientedLocation(Location):
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, o=Orientation.UNDEFINED):
        super().__init__(x, y, z)
        self.orientation = o


class AccessPoint:
    def __init__(self, mac: str, loc=Location(), p=20.0, a=5.0, f=2417000000):
        self.mac_address = mac
        self.location = loc
        self.output_power_dbm = p
        self.antenna_dbi = a
        self.output_frequency_hz = f


class APSample:
    """
        Class APSample defines a RSSI sample associated to an access point.
        RSSI values are contained in a list
    """

    def __init__(self, ap=AccessPoint("00:00:00:00:00:00")):
        self.access_point = ap
        self.rssi_values: list[float] = []

    """
        Converts RSSI values to an histogram.
        An histogram is stored in a dictionary whose keys are RSSI values
        and values are RSSI values occurrences
    """
    def to_histogram(self):
        histogram = {}
        for rssi in self.rssi_values:
            try:
                histogram[rssi] += 1
            except KeyError:
                histogram[rssi] = 1
        return histogram

    """
        Computes the average value for a list of RSSI values (by converting in mW prior to avg computation)
    """
    def to_average(self):
        rssi_mw = [10 ** (x / 10.0) for x in self.rssi_values]
        return 10 * log10(sum(rssi_mw) / len(rssi_mw))


class ReferencePoint:
    def __init__(self):
        self.location = Location()
        self.samples: list[APSample] = []

    def index_of_ap(self, mac_address: str):
        for i, m in enumerate(self.samples):
            if m.access_point.mac_address == mac_address:
                return i
        return -1

    def add_rssi_to_ap(self, rssi: float, mac_address: str):
        idx = self.index_of_ap(mac_address)
        if idx == -1:
            new_sample = APSample(AccessPoint(mac_address))
            new_sample.rssi_values.append(rssi)
            self.samples.append(new_sample)
        else:
            self.samples[idx].rssi_values.append(rssi)


class RSSI_Database:
    def __init__(self):
        self.reference_points: list[ReferencePoint] = []

    """
        Function import_from_file reads from file whose path is filename
        It builds a RSSIDatabase with one reference point for each oriented location (i.e. each CSV file line)
        Each reference point has one APSample for every distinct AP with samples.
    """
    def import_from_file(self, filename: str):
        with open(filename, newline='') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            for row in data:
                # Your code here
                pass

    """
        Function new_non_oriented_db creates and returns a new database with non-oriented locations
        Whenever similar locations (i.e. locations with the same x,y,z but different orientations) are
        found, they must be grouped in the same reference point.
    """
    def new_non_oriented_db(self):
        new_db = RSSI_Database()
        # Your code here
        return new_db
