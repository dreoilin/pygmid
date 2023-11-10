
def ngspice_parser(filename):
    
    selected_data = []
    with open(filename, 'r') as file:
        data = file.read().split()
        LENGTH = 34
        for i in range(0, len(data), LENGTH):  #34 because 34 columns of data
            section = [float(value) for value in data[i:i+LENGTH]]
            selected_data.append(list( section[j] for j in [0,1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33]))

    return selected_data