import csv
import numpy as np

def ngspice_parser(filename):
    
    with open(filename,'r') as csvfile:
        data = list(csv.reader(csvfile))
        data = np.array([[float(num) for num in line[0].split()] for line in data])
        data = np.delete(data, list(range(0, data.shape[1], 2)), axis=1).T
        
    return list(data)