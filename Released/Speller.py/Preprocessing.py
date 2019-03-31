import RawReader as reader

import numpy as np
from scipy.signal import butter,freqz,lfilter,hilbert
from matplotlib import pyplot as plt


from pylab import zeros,sin,kaiser,linspace,figure

def plot8row(dataset,y=None):
    l1,l2,l3 = dataset.shape
    for i in range(l1):
        plt.subplot(l1,1,1+i)
        if y != None:
            plt.ylim([-y,y])
        for j in range(l2):
            plt.plot(dataset[i,j])
    plt.show()

def butter_bandpass( lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandpass')
    return b, a


def KaiserFil(dataserie):
    import math
    pi = math.pi
    b = []
    fs=250
    cutoff=[0.5,4.0,7.0,12.0,30.0]
    y = dataserie
    filtered = []
    for band in range(len(cutoff) - 1):
        wl = 2 * cutoff[band] / fs * pi
        wh = 2 * cutoff[band + 1] / fs * pi
        M = 250  # Set number of weights as 128
        bn = zeros(M)
        for i in range(M):
            n = i - M / 2  # Make symmetrical
            if n == 0:
                bn[i] = wh / pi - wl / pi;
            else:
                bn[i] = (sin(wh * n)) / (pi * n) - (sin(wl * n)) / (pi * n)  # Filter impulse response
        bn = bn * kaiser(M, 5.2)
        b.append(bn)
        [w, h] = freqz(bn, 1)
        filtered.append(np.convolve(bn, y))
    #print(np.array(filtered).shape,"dd")
    return np.array(filtered)[:,M//2:M//2+1000]


###########################
def preprocess(path,training=True,index = 0,method = "FrequenzySeperated"):
    if training:
        Rawdata1 = reader.readdata(path)[index][:1000] # file name inlet
        bb, a = butter_bandpass(0.5, 30, 250, order=5)
        bandpassData = lfilter(bb, a, Rawdata1)
    elif not training:
        bandpassData = path

    else:
        raise "ParameterError training invalid"

    KaiserData = []

    if method == "BatchPhasePower":
        phaseData = np.array([np.unwrap(np.angle(hilbert(i))) for i in bandpassData])
        powerData = np.array([np.abs(hilbert(i)) for i in bandpassData])
        return (phaseData,powerData)
    elif method == "bandpass":
        return bandpassData

    elif method == "FrequenzySeperated":
        for i in range(8):
            KaiserData.append(KaiserFil(bandpassData[i]))
        KaiserData = np.array(KaiserData)
        #print(KaiserData.shape)
        #plot8row(KaiserData,12)
        phaseData = np.array([np.array([ np.unwrap(np.angle(hilbert(i))) for i in j]) for j in KaiserData])
        powerData = np.array([np.array([ np.abs(hilbert(i)) for i in j]) for j in KaiserData])
        return (KaiserData,phaseData,powerData)
    elif method == 'BatchPPFsep':
        for i in range(8):
            KaiserData.append(KaiserFil(bandpassData[i]))
        KaiserData = np.array(KaiserData)
        phaseData = np.array([np.unwrap(np.angle(hilbert(i))) for i in bandpassData])
        powerData = np.array([np.abs(hilbert(i)) for i in bandpassData])
        return KaiserData,phaseData,powerData
    else:
        raise "InvalidMethod"
    #print(phaseData.shape,powerData.shape,"phase power")#shape = (8,4,250)

    #plot8row(phaseData)
    #plot8row(powerData)
