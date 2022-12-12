from matplotlib import pyplot as plt
import random as rn
import numpy as np
 
import cmath
#16 Qam so far
def generarcadena(bits):
    ##Genero una cadena de bits aleatoria dependiendo de la cantidad de bits que el usuario em dio
    bits=int(bits)
    cadena = []
    final = [0]
    unos = np.ones(100, dtype=int)
    ceros = np.zeros(100, dtype=int)
    for i in range(0,bits):
        cadena.append(rn.randint(0,1))
    for i in cadena:
        if i==1:
            final=np.concatenate([final,unos])
        else:
            final=np.concatenate([final,ceros])
    return(final,cadena)
def demmaping(cadena):
    a=0.22
    b=0.82
    if cadena==[0,0,0,0]:
        complejo=0.82+0.82j
    elif cadena==[1,0,0,0]:
        complejo=0.82+0.22j
    elif cadena==[0,1,0,0]:
        complejo=0.82-0.22j
    elif cadena==[1,1,0,0]:
        complejo=0.82-0.82j
    elif cadena==[0,0,1,0]:
        complejo=0.22+0.82j
    elif cadena==[1,0,1,0]:
        complejo=0.22+0.22j
    elif cadena==[0,1,1,0]:
        complejo=0.22-0.22j
    elif cadena==[1,1,1,0]:
        complejo=0.22-0.82j
    elif cadena==[0,0,0,1]:
        complejo=-0.22+0.82j
    elif cadena==[1,0,0,1]:
        complejo=-0.22+0.22j
    elif cadena==[0,1,0,1]:
        complejo=-0.22-0.22j
    elif cadena==[1,1,0,1]:
        complejo=-0.22-0.82j
    elif cadena==[0,0,1,1]:
        complejo=-0.82+0.82j
    elif cadena==[1,0,1,1]:
        complejo=-0.82+0.22j
    elif cadena==[0,1,1,1]:
        complejo=-0.82-0.22j
    elif cadena==[1,1,1,1]:
        complejo=-0.82-0.82j
    
    return(complejo)
def senodesf(A, f, fs, phi, t):
    Ts=1/fs
    n=t/Ts
    n=np.arange(n)
    y=A*np.sin(2*np.pi*f*n*Ts + phi*(np.pi/180))
    return (y)
def arreglar(x):
    while (len(x)%4)!=0:
        x.append(0)
    return(x)
def QAM(cadena,x):
    puntos=[]
    compracion=[[0,0,0,0],[1,0,0,0],[0,1,0,0],[1,1,0,0],[0,0,1,0],[1,0,1,0],[0,1,1,0],[1,1,1,0],[0,0,0,1],[1,0,0,1],[0,1,0,1],[1,1,0,1],[0,0,1,1],[1,0,1,1],[0,1,1,1],[1,1,1,1]]
    x=arreglar(x)
    for i in compracion: 
        puntos.append(demmaping(i))
    ejex = [i.real for i in puntos] 
    ejey = [i.imag for i in puntos]      
    
    validar=[]
    complejos=[]
    for i in range(0,len(x),4):
        validar.append([x[i],x[i+1],x[i+2],x[i+3]])
    for i in validar:
        c1=demmaping(i)
        c2=complex(rn.gauss(0,0.05),rn.gauss(0,0.05))
        complejos.append((c1+c2))
    final=[0]
    for i in complejos:
        amplitud,phase=cmath.polar(i)    
        final=np.concatenate([final,senodesf(amplitud,1,500,-2*500*phase,1)])
    conruido=[]
    for i in range(0,len(final)):
        conruido.append(final[i]+rn.gauss(0,0.2))




    
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(final)    
    plt.grid()
    plt.subplot(3,1,2)
    plt.plot(cadena)    
    plt.grid()
    plt.subplot(3,1,3)
    plt.plot(conruido)    
    plt.grid()
    plt.show()

    ejex1 = [i.real for i in complejos] 
    ejey1 = [i.imag for i in complejos] 

    plt.figure()
    plt.subplot(2,1,1)    
    plt.scatter(ejex, ejey) 
    plt.ylabel('Imaginary') 
    #plt.xlabel('Real') 
    plt.title('Constelacion Ideal') 
    plt.grid()
    plt.subplot(2,1,2)
    plt.scatter(ejex1, ejey1) 
    plt.ylabel('Imaginary') 
    plt.xlabel('Real') 
    plt.title('Constelacion Real')
    plt.grid()
    plt.show()
    

    
    return
def validacionbits(bits):
    error=0
    try:
        bits=int(bits)
    except:
        error=1
    return(error)
def moddigitalQAM():
    bits=int(input('Ingrese el numero de bits: '))
    error=validacionbits(bits)
    
    if error==1:
        print('Error')
    else:
        cadena,x=generarcadena(bits)
        QAM(cadena,x)
    return()
moddigitalQAM()

## Codificación Manchester 

L = 32 # number of digital samples per data bit
Fs = 8*L # Sampling frequency
voltageLevel = 5 # peak voltage level in Volts
data = (np.random.rand(32)>0.5).astype(int) # random 1s and 0s for data
clk = np.arange(0,2*len(data)) % 2 # clock samples

ami = 1*data; previousOne = 0 

for ii in range(0,len(data)):
  if (ami[ii]==1) and (previousOne==0):
    ami[ii] = voltageLevel
    previousOne=1;
  if (ami[ii]==1) and (previousOne==1):
    ami[ii]= -voltageLevel
    previousOne = 0;
    clk_sequence = np.repeat(clk,L)
data_sequence = np.repeat(data,2*L)
manchester_encoded = voltageLevel* (2*np.logical_xor(data_sequence,clk_sequence).astype(int)-1)

fig, ax = plt.subplots(2,1,sharex='col', figsize=(7, 7))
ax[0].plot(data_sequence);ax[0].set_title('Data')
ax[1].plot(manchester_encoded); ax[1].set_title('Manchester Encoded - IEEE 802.3')
plt.show()