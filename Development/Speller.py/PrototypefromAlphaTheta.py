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

def p300():
    time.sleep(3)
    return("K")

def SI():
    global svc_clf, P300_clf
    ind = random.randint(0, 25)
    print("num =", ind)
    Series = np.load("../npSave/Pavarisa280219R06.npy")[ind, 0, :, :]
    print(np.asarray(Series).shape)
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
        typing = p300()
        while str(sock.recv(1024).decode("utf-8")).split(" ")[0]!="finished":
            print("wait ",end='')
        sock.send(("type "+typing).encode("utf-8"))
        print(("type "+typing).encode("utf-8"))
        #start p300 collect


        inp = None
    elif inp[0] == "wait":
        print("waiting")
