from pylsl import StreamInlet, resolve_stream
import socket
import Preprocessing as pre
import numpy as np
from sklearn.externals import joblib
import pickle
import random
import os
import time
import scipy as sp
from scipy.signal import butter,freqz,lfilter,hilbert
#########Develop Blink_seq&Blink_string##################
v = [1,2,3,4,5,6]
Blink_seq = []
trials = 3
for j in range(trials):
    for i in random.sample(v, len(v)):
        Blink_seq.append(i)
        Blink_seq.append(0)

Blink_string = ''
for Blink_number in Blink_seq:
    Blink_string = Blink_string+str(Blink_number)+','
Blink_string = Blink_string[:-1] #take the last ',' out
#########Develop Blink_seq&Blink_string##################



# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
print("No error")
streams = resolve_stream('type', 'EEG')
print("founded")
# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])
print(1)
sam_num = 0
Series = []
bb, a = pre.butter_bandpass(0.5, 30, 500, order=5)


#########Import model##################
svc_clf = joblib.load("weight2/weight_PavarisaNewUseRealSGD_1000_BatchPPFsep58.sav")
print(svc_clf)
P300_clf = joblib.load(open('finalized_p300model.sav', 'rb'))
#########Import model##################
print('models imported')

print('ready')
x=input("INSERT OK TO Start ")

print('starting')
#########Collecting Speech Imagery Data##################
while x == 'OK':
    
    sample, timestamp = inlet.pull_sample()
    Series.append(sample)
    sam_num = sam_num+1
    if sam_num == 1000:
        break
Series = np.asarray(Series).T
print(np.asarray(Series).shape)
#########Collecting Speech Imagery Data##################



#########Preprocess Data##################
bandpassData = pre.lfilter(bb, a, Series)
print(bandpassData.shape)
KaiserData = []
for i in range(8):
    tmp = pre.KaiserFil(bandpassData[i])
    KaiserData.append(tmp)
#FeaturedData = multibandfeat(KaiserData)
#print(np.asarray(KaiserData).shape)
#print("FeaturedData",len(FeaturedData))
#KaiserData = np.array(KaiserData)
KaiserData = np.array(KaiserData)
phaseData = np.array([np.unwrap(np.angle(hilbert(i))) for i in bandpassData])
powerData = np.array([np.abs(hilbert(i)) for i in bandpassData])
data = []
for i in range(8):
    for j in range(4):
        data.append(KaiserData[i][j])
        data.append(phaseData[i])
        data.append(powerData[i])
print("aaa",aaa.shape)
#shape=(8,4,1000)
#########Preprocess Data##################
A = np.reshape(aaa, (1, -1)) #(1,samnum) array
print("A",A.shape)
#########Predict for SI_Result##################
Seq = []
output = svc_clf.decision_function(A)#np.array([FeaturedData]))[0]
print("output",output.shape)
print(output)
for j in range(26):
    Seq.append([-output[0][j],j])#กำกับ percentage ด้วย Alphabet_index
Seq.sort() #sort percentage
SI_result = ''
for t in Seq[0:9]: #เลือก 9 ตัวที่มี percent มากสุด
        SI_result=SI_result+'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[t[1]] #แปรผลเป็นตัวอักษรimport socket
#########Predict for SI_Result##################


print('Result:'+SI_result)

#########Set up Server for Processing##################
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2.bind(("127.0.0.1", 5001))   

    #########Open Processing##########
sock2.listen(1) #ต้องเช็คอีกรอบ########
os.chdir("application.windows64")
os.system("The_speller.exe")
os.chdir("../")
#########Open Processing##################


conn2, addr2 = sock2.accept() #ต้องเช็คอีกรอบ
#########Set up Server for Processing##################

print('Connected by', addr2)
print('sending Result to Processing')
    
#########Send Result&Blink_string##################
arr = bytes(SI_result+Blink_string, 'utf-8')
conn2.sendall(arr)
#########Send Result&Blink_string##################

sample_num = 0
P300_data=[]
P300new=[]
#########Collecting Data while flashing##################
while True:
    data = str(repr(conn2.recv(1024)))[2:-1]
    print(data)
    if data=="Start" :
        print("ok")
        break

while True:
    sample, timestamp = inlet.pull_sample()
    P300_data.append(sample)
    #print("appended",sample)
    sample_num=sample_num+1
    time.sleep(0.004)
    if sample_num==465:
        break

#########Collecting Data while flashing##################
print(len(Blink_seq))
#########Predict P300_result##################
P300 = np.array(P300_data).T
print(type(P300),P300.shape)
new_P300 = []
for blink in range(18):
    tmps = []
    for node in range(8):
        #print(len(P300[node][50+20*blink:125+20*blink]),"ist",blink,node)
        tmps+=list(P300[node][50+20*blink:125+20*blink])
    #print(tmps)
    new_P300+=[tmps]
new_P300=np.array(new_P300)
#Data_shape = (18 blinks*8 nodes*3trials,75)
P300_result = P300_clf.decision_function(new_P300)
#########Predict P300_result##################

print(P300_result)

#########แปรผล##################
row_column = []
for i in range(18):
    if P300_result[i]<=0:
        row_column.append(Blink_seq[2*i])
print(len(row_column),'*')
for i in range(int(len(row_column)/2)):
    row = sorted(row_column[2*i:2*i+2])[0] #row will be 4-6
    column = sorted(row_column[2*i:2*i+2])[1] #column will be 1-3
    print(SI_result[(row-4)*3+column])
#########แปรผล##################