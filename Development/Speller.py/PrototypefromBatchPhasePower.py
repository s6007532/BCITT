import socket

HOST = '127.0.0.1'                 # Symbolic name meaning all available interfaces
PORT = 5000              # Arbitrary non-privileged port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
sock, addr = server.accept()

from pylsl import StreamInlet, resolve_stream
import os
print(os.getcwd())
import Preprocessing as pre
print("hi")
import numpy as np
from sklearn.externals import joblib
import random
import os
import time
import scipy as sp
from scipy.signal import butter,freqz,lfilter,hilbert


svc_clf = joblib.load("weight_PavarisaNewUseRealSGD_1000_BatchPhasePower52.sav")
print(svc_clf)
P300_clf = joblib.load(open('finalized_p300model.sav', 'rb'))
print("model imported")
##will be changed into stream capturing

#blinksq = ['r0', 'r1', 'r2', 'c0', 'c1', 'c2',]
blinksq = ['r0,r0,r0', 'r1,r1,r1', 'r2,r2,r2', 'c0,c0,c0', 'c1,c1,c1', 'c2,c2,c2']

print('Connected by', addr)

def p300(Blink_seq,SI_result):
    bypass=True
    global P300_clf
    sample_num = 0
    P300_data = []

    if not bypass:
        while True:
            sample, timestamp = inlet.pull_sample()
            P300_data.append(sample)
            # print("appended",sample)
            sample_num = sample_num + 1
            time.sleep(0.004)
            if sample_num == 465:
                break
    else:
        ind = random.randint(0, 25)
        print("num =", ind)
        Series = np.load("../npSave/Pavarisa280219R06.npy")[ind, 0, :, :465]
        print(np.asarray(Series).shape)
        P300_data = Series
        
    #########Collecting Data while flashing##################
    print(len(Blink_seq))
    
    #########Predict P300_result##################
    P300 = np.array(P300_data).T
    print(type(P300), P300.shape)
    new_P300 = []
    for blink in range(18):
        tmps = [] #contain data of every node for one blink
        for node in range(8):
            # print(len(P300[node][50+20*blink:125+20*blink]),"ist",blink,node)
            tmps += list(P300[node][50 + 20 * blink:125 + 20 * blink]) #200 - 500 ms (since data is digitalized at 250Hz)
        # print(tmps)
        new_P300 += [tmps]
    new_P300 = np.array(new_P300) #shape = (18,600)
    P300_result = P300_clf.decision_function(new_P300)
    #########Predict P300_result##################

    #########แปรผล##################
    H = {'r0':4, 'r1':5, 'r2':6, 'c0':1, 'c1':2, 'c2':3}
    for i in range(len(Blink_seq)):
        Blink_seq[i] = H[Blink_seq[i]] 
    #print(new_Blink_seq) #will be in form of [1,2,3,4,5,6]
    Prob = [[0,1],[0,2],[0,3],[0,4],[0,5],[0,6]]
    for i in range(len(Blink_seq)):
        Prob[Blink_seq[i]-1][0] += P300_result[i] #sum up probs from different blinks
    #Prob will be like this :[[-5.644267831120814, 4], [-11.492414954500223, 5], [-15.265074033861413, 6],[-16.30554780973207, 1], [-5.209323588360705, 2], [-1.958844355953289, 3]]
    row_result = [] #contain probs for column
    column_result = [] #contain probs for row
    for i in Prob:
        if i[1] <=3:
            column_result.append(i) 
            #[[-5.644267831120814, 4], [-11.492414954500223, 5], [-15.265074033861413, 6]]
        else:
            row_result.append(i) 
            #[[-16.30554780973207, 1], [-5.209323588360705, 2], [-1.958844355953289, 3]]
    row = sorted(row_result)[-1][1] #find row with the highest prob  
    column = sorted(column_result)[-1][1] #find column with the highest prob
    #########แปรผล##################
    return(SI_result[(row-4)*3+column-1])

def SI():
    global svc_clf
    ind = random.randint(0, 25)
    print("num =", ind)
    Series = np.load("../npSave/Pavarisa280219R06.npy")[ind, 0, :, :]
    print(np.asarray(Series).shape)
    """
    while x == 'OK':
        sample, timestamp = inlet.pull_sample()
        Series.append(sample)
        sam_num = sam_num+1
        if sam_num == 1000:
            break
    Series = np.asarray(Series).T
    print(np.asarray(Series).shape)"""

    bb, a = pre.butter_bandpass(0.5, 30, 500, order=5)
    bandpassData = pre.lfilter(bb, a, Series)
    print(bandpassData.shape)
    KaiserData = []
    for i in range(8):
        tmp = pre.KaiserFil(bandpassData[i])
        KaiserData.append(tmp)
    phaseData = np.array([np.unwrap(np.angle(hilbert(i))) for i in bandpassData])
    powerData = np.array([np.abs(hilbert(i)) for i in bandpassData])
    aaa = np.ravel((phaseData, powerData))
    A = np.reshape(aaa, (1, -1))
    Seq = []
    output = svc_clf.decision_function(A)  # np.array([FeaturedData]))[0]
    for j in range(26):
        Seq.append([-output[0][j], j])
    Seq.sort()  # sort percentage
    SI_result = ''
    for t in Seq[0:9]:  # เลือก 9 ตัวที่มี percent มากสุด
        SI_result = SI_result + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[t[1]]  # แปรผลเป็นตัวอักษรimport socket
    print('Result:' + SI_result)
    return SI_result

print("ready")
sock.send(b"ready")

while True:
    inp = str(sock.recv(1024).decode("utf-8")).split(" ")
    if inp[0] == "collect":
        results = SI()# SI processing
        random.shuffle(blinksq)
        ret = (results + " " + ",".join(blinksq)).encode("utf-8")
        print(ret)
        sock.send(ret)
        typing = p300(["we"])
        while str(sock.recv(1024).decode("utf-8")).split(" ")[0]!="finished":
            print("wait ",end='')
        sock.send(("type "+typing).encode("utf-8"))
        print(("type "+typing).encode("utf-8"))
        #start p300 collect


        inp = None
    elif inp[0] == "wait":
        print("waiting")
