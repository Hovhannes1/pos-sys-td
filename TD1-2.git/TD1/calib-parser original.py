import csv
import sys
from math import log10

def usage(name):
    print("Usage: " + name + " <input file>")




"""
	Class RSSISample defines a sample with its source MAC address (in text)
	and an array of RSSI values (in dBm, values are stored in floating point)
	An instance of this class will belong to a RSSIRecord in the DB
"""
class RSSISample():
	def __init__(self, macaddr):
		self.macaddr = macaddr
		self.rssi = []

		
	def addSample(self, macaddr, rssi):
		if (self.macaddr == macaddr):
			self.rssi.append(rssi)

	
	"""
		This function goes through the RSSI values array of the object, converts its
		dBm values to mW, then computes the average value, and finally returns the
		average value in dBm (so you must convert it back to dBm)
		
		Return the average RSSI value in dBm
	"""	
	def computeAverageValue(self):
		# Your code goes here
		return None # Change return value according to your code

		
	def __eq__(self, other):
		return self.macaddr==other.macaddr
		
		
	def __ne__(self, other):
		return not self.__eq__(other)
		
		
	def __lt__(self, other):
		return self.macaddr.upper() < other.macaddr.upper()
		
		
	def __le__(self, other):
		return self.macaddr.upper() <= other.macaddr.upper()
		
		
	def __gt__(self, other):
		return self.macaddr.upper() > other.macaddr.upper()


	def __ge__(self, other):
		return self.macaddr.upper() >= other.macaddr.upper()


	def __str__(self):
		return str({'macaddr': self.macaddr, 'rssi': self.rssi})
		
		
	def __repr__(self):
		return self.__str__()
	
	
	
		
"""
	Class RSSIRecord contains a location and all its RSSI samples
	Its location is defined by members x, y, z, orientation (float values)
	It keeps its RSSISample samples in the member array 'samples'
"""
class RSSIRecord():
	def __init__(self, x, y, z, o):
		self.x = x
		self.y = y
		self.z = z
		self.orientation = o
		self.samples = []
	
	
	"""
		This function adds a new sample to the record. The sample is defined
		by its source MAC address and its RSSI value.
		If the source MAC address already exists in the record, it must be
		updated by appending the new RSSI value to the existing ones
		If not, a new sample must be appended to the record samples.
	"""
	def addSample(self, macaddr, rssi):
		# Your code goes here
		pass # Remove after completion
			
			
	def __eq__(self, other):
		return self.x==other.x and self.y==other.y and self.z==other.z and self.orientation==other.orientation
		
		
	def __ne__(self, other):
		return not self.__eq__(other)
		
		
	def __lt__(self, other):
		if self.x < other.x:
			return True
		elif self.x > other.x:
			return False
		if self.y < other.y:
			return True
		elif self.y > other.y:
			return False
		if self.z < other.z:
			return True
		elif self.z > other.z:
			return False
		if self.orientation < other.orientation:
			return True
		elif self.orientation > other.orientation:
			return False
		return False
		
		
	def __le__(self, other):
		return self.__lt__(other) or self.__eq__(other)
		
		
	def __gt__(self, other):
		return not self.__le__(other)
		
		
	def __ge__(self, other):
		return not self.__lt__(other)
		
		
	def __repr__(self):
		return str({'x': self.x, 'y': self.y, 'z': self.z, 'orientation': self.orientation, 'samples': self.samples})
		
		
	def __str__(self):
		return self.__repr__()
		
		
		
		
"""
	Class RSSIDatabase manages an array of records (one per calibration location)
"""
class RSSIDatabase():
	def __init__(self):
		self.database = []
		
		
	def __repr__(self):
		return str({'database': self.database})
	
		
	def __str__(self):
		return self.__repr__()
	
	
	"""
		Function importCsvFile imports a CSV file to the RSSI DB while converting
		CSV data to instances of RSSIRecord and RSSISample
		
		Parameter file_name is the path to the input CSV file
		
		Remember to check the unicity of your x, y, z records (with orientation
		set to 0 whatever the source value), and to add or update records
		according to this constraint:
			- if a record for current location already exists, update it
			- if not, create a new one and insert current samples into it
	"""
	def importCsvFile(self, file_name):
		# Your code goes here
		pass # Remove to use your code


	"""
		Function saveToCsv saves your RSSI database to a CSV file
		
		Parameter file_name is the path to the output file
		
		Do not forget to save only one RSSI value (the average value) for each
		sample in your RSSI database
	"""			
	def saveToCsv(self, file_name):
		# Your code goes here
		pass # Remove to use your code




def main():
	if (len(sys.argv) != 2):
		usage(sys.argv[0])
		exit(-1)
	my_rssi_db = RSSIDatabase()
	my_rssi_db.importCsvFile(sys.argv[1])
	output_name = sys.argv[1][:-3] + 'out.csv'
	my_rssi_db.saveToCsv(output_name)


main()
