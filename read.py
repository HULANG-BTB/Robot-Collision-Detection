import numpy as np

def readData() :
    ret = []
    file = open("trainInput.txt", "r")
    for line in file:
        ret.append([float(x) for x in line.split()])
    file.close()
    result = []
    for i in range(5, len(ret)) :
        result.append([ret[i-4], ret[i-3], ret[i-2], ret[i-1], ret[i]])
    return result

if __name__ == "__main__":
    ret = np.array(readData())
    print(ret.shape)
