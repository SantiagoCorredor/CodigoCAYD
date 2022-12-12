import random

import numpy as np

from sk_dsp_comm import digitalcom

from matplotlib import pyplot as plt

import cmath

from scipy.fftpack import fft, fftfreq


def main():
    n=int(input('Ingrese el numero de canales (maximo 12) = '))
    if n > 12:
        print('problema')
    else:
        FDM(n)


def FDM(n):
    fs=12000
    F=np.linspace(1,4,n)
    tonos_prueba=[]
    portadoras=[]  
    for i in F:
        tonos_prueba.append(sin_wave(1,0,i,fs,1))
        
        

    Fc=[(100-4*i) for i in range(0,n)]

    for i in Fc:
        portadoras.append(sin_wave(1,0,i,fs,1))
      
    ampaso=[]
    am_señaes=[]
    for i in range(0,n):
        for j in range(0,len(tonos_prueba[i])):
            ampaso.append(tonos_prueba[i][j]*portadoras[i][j])
        
        am_señaes.append(list(ampaso))
        ampaso.clear()

    final=[]
    temp=0
    for i in range(0,len(tonos_prueba[0])):
        temp=0
        for j in range(0,n):
            temp=temp+am_señaes[j][i]
        final.append(temp)
    #Señales de entrada.
    plt.figure()

    plt.subplot(141)
    plt.plot(am_señaes[0])
    plt.subplot(142)
    plt.plot(am_señaes[1])
    plt.subplot(143)
    plt.plot(am_señaes[3])
    plt.subplot(144)
    plt.plot(am_señaes[4])
    
    plt.subplot(241)
    plt.plot(am_señaes[5])
    plt.subplot(242)
    plt.plot(am_señaes[6])
    plt.subplot(243)
    plt.plot(am_señaes[7])
    plt.subplot(244)
    plt.plot(am_señaes[8])
    
    plt.subplot(341)
    plt.plot(am_señaes[9])
    plt.subplot(342)
    plt.plot(am_señaes[10])
    plt.subplot(343)
    plt.plot(am_señaes[11])
    
    plt.figure(0)
    plt.plot(final)
    plt.show()
    
    yf = fft(final)
    xf = fftfreq(fs, 1/fs)[:fs//2]
    
    plt.stem(xf, 2.0/fs * np.abs(yf[0:fs//2]))
    plt.xlim(0,120)
    plt.grid()
    plt.show()
    
    return

def sin_wave(A,phi,F,fs,t):
    Ts = 1/fs
    n = t / Ts
    n = np.arange(n)
    y = A*np.sin(2*np.pi*F*n*Ts + phi*(np.pi/180))
    return y

    
main()