from matplotlib import pyplot as plt
import numpy as np

def readfrommap(mapf):
    f = open(mapf)
    lf = f.readlines()
    tmp = []
    for  i in lf:
        pack = readpack(i)
        tmp.append(pack)
    return np.array(tmp)

def savefrommap(mapf):
    f = open(mapf)
    lf = f.readlines()
    for i in lf:
        savepack(i[:-1])

def readpack(packname):
    from string import ascii_uppercase as upcase
    tmp =[]
    for i in upcase:
        tmp+= [readdata("saves/"+packname+"-"+i+".txt")]
    return np.array(tmp)


def savepack(packname):
    pack = readpack(packname)
    np.save("npSave/"+packname+".npy",pack)

def readdata(path,straight = True):
    if straight:
        from scipy import signal as sg
        from matplotlib import pyplot as plt

    dset = []
    # num dataset
    # dtf = open("..\save\\"+alph+".txt").read().split('#')
    dtf = open(path).read().split('#')
    dtf.pop(0)
    # print(dtf)
    for c in dtf:
        #tttt=[]
        pdset = [[],[],[],[],[],[],[],[]]
        #print("init",pdset)
        #print(c.strip()+'hello')
        if c == "":
            break
        #print('sample rows : ',len(c.strip().split("\n")))
        count =0
        for i in c.strip().split("\n"):
            count += 1
            #print(i,"ll")
            packt=[]
            for j in range(1,9) :
                rowmember = i.split(",")[j]

                pdset[j-1]+=[float(rowmember)]

#        print(np.array(pdset).shape,"shape", count)
        dset.append(pdset)

    dset = np.array(dset)
    #print(dset.shape)


    #print("read ",dset.shape," RawReader")
    baselines=[]
    for k in range(len(dset)):
        baselinepack = []
        for i in range(8):
            mean = np.mean(dset[k, i])
            dset[k, i] -= mean
            if straight:
                baseline = sg.medfilt(dset[k, i],125)
                baselinepack.append(baseline)

                #plt.plot(baseline)
                #plt.show()
        baselines.append(baselinepack)
    baselines = np.array(baselines)
    #print(baselines.shape)
    dset-=baselines
    #print(dset[:])

    return (dset) #(n=2, 8, 250)
"""
dataArraySet = readdata("saves/song1710-A.txt")[0]
plt.plot(dataArraySet.T)
plt.show()
"""