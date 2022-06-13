import csv
import sys
from math import log10

def usage(name):
    print("Usage: " + name + " <input file>")

'''Class RSSISample defines a sample with its source MAC address (in text)
	and an array of RSSI values (in dBm, values are stored in floating point)
	An instance of this class will belong to a RSSIRecord in the DB'''

class RSSISample():
    def __init__(self,macaddr):
        self.macaddr = macaddr
        self.rssi = []
        
    def addSample(self, macaddr, rssi):
        if (self.macaddr == macaddr):
            self.rssi.append(rssi)
            
    '''
    This function goes through the RSSI values array of the object, converts its
		dBm values to mW, then computes the average value, and finally returns the
		average value in dBm (so you must convert it back to dBm)
		
		Return the average RSSI value in dBm
    '''
        
    def computeAverageValue(self):
        sum_mw = 0
        for x in range(0,len(self.rssi),1):
            sum_mw+=pow(10,float(self.rssi[x])/10)
        return 10*log10(sum_mw)
        
    
    def __eq__(self,other):
        return self.macaddr==other.macaddr
    
    def __ne__(self,other):
        return not self.__eq__(other)
    
    def __lt__(self,other):
        return self.macaddr.upper() < other.macaddr.upper()
    
    def __le__(self,other):
        return self.macaddr.upper() <= other.macaddr.upper()
    
    def __gt__(self,other):
        return self.macaddr.upper() > other.macaddr.upper()
    
    def __ge__(self, other):
        return self.macaddr.upper() >= other.macaddr.upper()
    
    def __str__(self):
        return str({'macaddr': self.macaddr, 'rssi': self.rssi})
    
    def __repr__(self):
        return self.__str__()
    '''
    Class RSSIRecord contains a location and all its RSSI samples
	Its location is defined by members x, y, z, orientation (float values)
	It keeps its RSSISample samples in the member array 'samples'
    '''
    
class RSSIRecord():
    def __init__(self, x, y, z, o):
        self.x = x
        self.y = y
        self.z = z
        self.orientation = o
        self.samples = []
    '''
    This function adds a new sample to the record. The sample is defined
		by its source MAC address and its RSSI value.
		If the source MAC address already exists in the record, it must be
		updated by appending the new RSSI value to the existing ones
		If not, a new sample must be appended to the record samples.
    '''
    def addSample(self, macaddr, rssi):
        exist = False
        j=0
        while j < len(self.samples ) and not exist:
            if (self.samples[j].macaddr == macaddr):
                exist=True
            else:
                j = j+1
        if (not exist):
            sample = RSSISample(macaddr)
            sample.addSample(macaddr, rssi)
            self.samples.append(sample)
        else:
            self.samples[j].addSample(macaddr,rssi)
                
        
    def sortAscending(self):
        self.samples = sorted(self.samples, key=lambda sample: sample.macaddr)
    
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

'''Class RSSIDatabase manages an array of records (one per calibration location)'''

class RSSIDatabase():
    def __init__(self):
        self.database = []
    
    def __repr__(self):
        return str({'database': self.database})
    
    def __str__(self):
        return self.__repr__()
    
    '''
		Function importCsvFile imports a CSV file to the RSSI DB while converting
		CSV data to instances of RSSIRecord and RSSISample
		
		Parameter file_name is the path to the input CSV file
		
		Remember to check the unicity of your x, y, z records (with orientation
		set to 0 whatever the source value), and to add or update records
		according to this constraint:
			- if a record for current location already exists, update it
			- if not, create a new one and insert current samples into it
    '''
                
    def importCsvFile(self, file_name):
      with open(file_name, 'r') as file:
        my_reader = csv.reader(file, delimiter=',')
        count = 0
        i = -1
        for row in my_reader:
          if (count == 0):
              self.database.append(RSSIRecord(row[0], row[1], row[2], 0))
              i = i+1
          for x in range(4,len(row),2):
              self.database[i].addSample(row[x],row[x+1])
          count=count+1
          if(count==4):
              self.database[i].sortAscending()
              count = 0
                  
                      
                      
                  
                      
          
    
    
    '''
    Function saveToCsv saves your RSSI database to a CSV file
		
		Parameter file_name is the path to the output file
		
		Do not forget to save only one RSSI value (the average value) for each
		sample in your RSSI database
    '''


    def saveToCsv(self, file_name):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file,delimiter=',')
            data = []
            
            for i in range(0,len(self.database),1):
                data.append(str(self.database[i].x))
                data.append(str(self.database[i].y))
                data.append(str(self.database[i].z))
                data.append(str(self.database[i].orientation))
                
                for k in range(0,len(self.database[i].samples),1):
                    data.append(str(self.database[i].samples[k].macaddr))
                    data.append("{0:.3f}".format(self.database[i].samples[k].computeAverageValue()))
                writer.writerow(data)
                data.clear()
            
    
def main():
    if(len(sys.argv) != 2):
        usage(sys.argv[0])
        exit(-1)
    my_rssi_db = RSSIDatabase()
    my_rssi_db.importCsvFile(sys.argv[1])
    output_name = sys.argv[1][:-3] + 'out.csv'
    my_rssi_db.saveToCsv(output_name)

main()