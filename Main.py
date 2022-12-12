import tkinter
import customtkinter
import matplotlib.pyplot as plt
from tkinter import *

from commpy.utilities import upsample

import numpy as np

import random as rn
import cmath

from scipy import *
from scipy.special import erfc

from sk_dsp_comm.digitalcom import sqrt_rc_imp

from scipy.fftpack import fft, fftfreq



customtkinter.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

menu = customtkinter.CTk()
menu.geometry("360x360")
menu.resizable(width=False, height=False)
menu.title("Parcial rescate")

app_linea = customtkinter.CTk()
app_linea.geometry("350x280")
app_linea.resizable(width=False, height=False)
app_linea.title("Codificación Manchester")

app_canal = customtkinter.CTk()
app_canal.geometry("350x530")
app_canal.resizable(width=False, height=False)
app_canal.title("Codificador Hamming(11,7)")

app_mod_dig = customtkinter.CTk()
app_mod_dig.geometry("350x300")
app_mod_dig.resizable(width=False, height=False)
app_mod_dig.title("Modulador digital 16 - QAM")

app_mult = customtkinter.CTk()
app_mult.geometry("350x300")
app_mult.resizable(width=False, height=False)
app_mult.title("Simulador multiplexado FDM")

app_acc_mult = customtkinter.CTk()
app_acc_mult.geometry("350x300")
app_acc_mult.resizable(width=False, height=False)
app_acc_mult.title("Simulador Acceso multiple")


def linea(): 
    app_linea.mainloop()
    
def canal():
    app_canal.mainloop()

    
    
def qam_16():
    app_mod_dig.mainloop()
    
    
def fdm_acc():
  app_mult.mainloop()
    
def tdma():
  app_acc_mult.mainloop()
  

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
    plt.plot(final);plt.title("Salida QAM") 
    plt.grid()
    plt.subplot(3,1,2);plt.title("Entrada de datos")
    plt.plot(cadena)    
    plt.grid()
    plt.subplot(3,1,3);plt.title("Salida QAM con ruido")
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
    bits=int(entry_5.get())
    error=validacionbits(bits)
    
    if error==1:
        error_5 = customtkinter.CTkLabel(master=frame_4, text="Bits incorrecros (2^m)", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
        error_5.place(x=55, y=92)
    else:
        cadena,x=generarcadena(bits)
        QAM(cadena,x)
    return()

def button_callback():
  Hamming = [None, None, None, None, None, None, None, None, None, None, None]
  salidaHm = ''
  flag2, p0, p1, p2, p3 = 0, None, None, None, None
  P0 = [7,6,4,3,1]
  P1 = [7,5,4,2,1]
  P2 = [6,5,4]
  P3 = [3,2,1]
  
  def paridad(Pn):  #devuelve el bit de paridad, se ingresan las posiciones que controla Pn
    cont = 0
    p = 2
    for n in range(0,len(Pn)):
      if((ms[Pn[n]-1])=='1'):
        cont = cont + 1
    if((cont%2)!=0):
      p = 1
    else:
      p = 0
    return p
   
  ms = entry_1.get()
  flag1 = len(ms)
  if (flag1!=7): #valida que sean 7 elementos
    error_1 = customtkinter.CTkLabel(master=frame_3, text="Longitud errada", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
    error_1.place(x=15, y=50)
  else:
    error_1 = customtkinter.CTkLabel(master=frame_3, text="", font=("Roboto Medium", -2) ,justify=tkinter.LEFT)
    error_1.place(x=15, y=50)
    for n in range(0,7):    #valida que sean solo 1's o 0's.
      if ((ms[n]=='0') or (ms[n]=='1')):
        flag2 = flag2 + 1
      else:
        flag2 = 0

    if (flag2 != 7):
      error_1 = customtkinter.CTkLabel(master=frame_3, text="El mensaje no esta escrito en binario, escriba solo 1's o 0's", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
      error_1.place(x=15, y=50)  
      
    else:
      error_1 = customtkinter.CTkLabel(master=frame_3, text="                                ", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
      error_1.place(x=15, y=50)
      p0 = paridad(P0)
      p1 = paridad(P1)
      p2 = paridad(P2)
      p3 = paridad(P3)
      Hamming[0]=int(ms[0])
      Hamming[1]=int(ms[1])
      Hamming[2]=int(ms[2])
      Hamming[3]=p3
      Hamming[4]=int(ms[3])
      Hamming[5]=int(ms[4])
      Hamming[6]=int(ms[5])
      Hamming[7]=p2
      Hamming[8]=int(ms[6])
      Hamming[9]=p1
      Hamming[10]=p0
      salidaHm = ms[0]+ ms[1]+ ms[2]+str(p3)+ms[3]+ms[4]+ms[5]+str(p2)+ms[6]+str(p1)+str(p0)   
      entry_2.delete(0, 11)
      entry_2.insert(0, salidaHm)

def button_gen_error():
  ms = entry_2.get()
  flag1 = len(ms)
  flag6 = 0
  if (flag1!=11): #valida que sean 11 elementos
    error_2 = customtkinter.CTkLabel(master=frame_3, text="La longitud es erronea", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
    error_2.place(x=75, y=180)
  else:
    error_2 = customtkinter.CTkLabel(master=frame_3, text="", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
    error_2.place(x=75, y=180)
    for n in range(0,len(ms)):    #valida que sean solo 1's o 0's.
      if ((ms[n]=='0') or (ms[n]=='1')):
        flag6 = flag6 + 1
      else:
        flag6 = 0

    if (flag6 != 11):
      error_2 = customtkinter.CTkLabel(master=frame_3, text="El mensaje no esta escrito en binario, escriba solo 1's o 0's", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
      error_2.place(x=75, y=180)  
      
    else:
      error_2 = customtkinter.CTkLabel(master=frame_3, text=" ", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
      error_2.place(x=75, y=180)

      listams = list(ms)
      poserror = rn.randint(0, 10)
         
      if (listams[poserror]=='1'):
        listams[poserror]='0'
      else:
        listams[poserror]='1'
        
      new_str = ''.join(listams)
      entry_3.delete(0, 11)
      entry_3.insert(0, new_str)
      label_4 = customtkinter.CTkLabel(master=frame_3, text="Error generado en la posicion: "+str(abs(10-11-poserror))+"                                                            ", font=("Roboto Medium", -10) ,justify=tkinter.LEFT)
      label_4.place(x=75, y=180)
           
def corrector():    
  ms = entry_3.get()
  flag1 = len(ms)
  flag2 = 0
  if (flag1!=11): #valida que sean 11 elementos
    error_3 = customtkinter.CTkLabel(master=frame_3, text="Longitud erronea", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
    error_3.place(x=75, y=300)
  else:
    error_3 = customtkinter.CTkLabel(master=frame_3, text="", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
    error_3.place(x=75, y=300)
    for n in range(0,11):    #valida que sean solo 1's o 0's.
      if ((ms[n]=='0') or (ms[n]=='1')):
        flag2 = flag2 + 1
      else:
        flag2 = 0

    if (flag2 != 11):
      error_3 = customtkinter.CTkLabel(master=frame_3, text="El mensaje no esta escrito en binario, escriba solo 1's o 0's", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
      error_3.place(x=75, y=300)  
      
    else:
      error_3 = customtkinter.CTkLabel(master=frame_3, text="                                                                                                                            ", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
      error_3.place(x=75, y=300)
      listms = list(ms)
      list2 = []
      for n in range(0,len(listms)):
        list2.append(int(listms[n]))
      
      p0 = list2[10]^list2[8]^list2[6]^list2[4]^list2[2]^list2[0]
      p1 = list2[9]^list2[8]^list2[5]^list2[4]^list2[1]^list2[0]
      p2 = list2[7]^list2[6]^list2[5]^list2[4]
      p3 = list2[3]^list2[2]^list2[1]^list2[0]
      perrorstr = str(p3)+str(p2)+str(p1)+str(p0)
      numero_decimal = 0 
      for posicion, digito_string in enumerate(perrorstr[::-1]):
        numero_decimal += int(digito_string) * 2 ** posicion
  
      if (list2[11-numero_decimal]==1):
        list2[11-numero_decimal] = 0
      else:
        list2[11-numero_decimal] = 1
      
      hmgc = str(list2[0])+str(list2[1])+str(list2[2])+str(list2[3])+str(list2[4])+str(list2[5])+str(list2[6])+str(list2[7])+str(list2[8])+str(list2[9])+str(list2[10])
      
      entry_4.delete(0, 11)
      entry_4.insert(0, hmgc)
      label_6 = customtkinter.CTkLabel(master=frame_3, text="Se detecto error en la posicion "+str(abs(12-numero_decimal))+" y se corrigio      ", font=("Roboto Medium", -10) ,justify=tkinter.LEFT)
      label_6.place(x=25, y=420)
      
def button_dig():
  moddigitalQAM()

def Manchester():
  L = 32 # number of digital samples per data bit
  Fs = 8*L # Sampling frequency
  voltageLevel = 5 # peak voltage level in Volts
  
  data = (np.random.rand(int(entry_bits_cl.get()))>0.5).astype(int) # random 1s and 0s for data
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
  alpha = float(entry_roll_off.get())
  rcosalz = sqrt_rc_imp(32, alpha) 
  banda_b = np.convolve(manchester_encoded, rcosalz)

  fig, ax = plt.subplots(3,1, figsize=(7, 10))
  ax[0].plot(data_sequence);ax[0].set_title('Data')
  ax[1].plot(manchester_encoded); ax[1].set_title('Manchester Encoded - IEEE 802.3')  
  ax[2].plot(banda_b);ax[2].set_title("Señal pasada por el filtro coseno")
  plt.show()

def FDM():
  n = int(entry_multi_canal.get())
  if(n > 12 and n < 2):
    error_6 = customtkinter.CTkLabel(master=frame_5, text="Max 12", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
    error_6.place(x=55, y=92)
    app_mult.destroy.pack()
    return 0
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
  if (n == 2):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(7, 10))
    ax[0].plot(am_señaes[0])
    ax[0].set_title('Señal 1')
    ax[1].plot(am_señaes[1])
    ax[1].set_title('Señal 2')
    plt.show()

  if (n == 3):
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(7, 10))
    ax[0, 0].plot(am_señaes[0])
    ax[0, 0].set_title('Señal 1')
    ax[0, 1].plot(am_señaes[1])
    ax[0, 1].set_title('Señal 2')
    ax[0, 2].plot(am_señaes[2])
    ax[0, 2].set_title("Señal 3")
    plt.show()

  if (n == 4):
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(7, 10))
    ax[0, 0].plot(am_señaes[0])
    ax[0, 0].set_title('Señal 1')
    ax[0, 1].plot(am_señaes[1])
    ax[0, 1].set_title('Señal 2')
    ax[0, 2].plot(am_señaes[2])
    ax[0, 2].set_title("Señal 3")
    ax[1, 0].plot(am_señaes[3])
    ax[1, 0].set_title("Señal 4")
    plt.show()

  if (n == 5):
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(7, 10))
    ax[0, 0].plot(am_señaes[0])
    ax[0, 0].set_title('Señal 1')
    ax[0, 1].plot(am_señaes[1])
    ax[0, 1].set_title('Señal 2')
    ax[0, 2].plot(am_señaes[2])
    ax[0, 2].set_title("Señal 3")
    ax[1, 0].plot(am_señaes[3])
    ax[1, 0].set_title("Señal 4")
    ax[1, 1].plot(am_señaes[4])
    ax[1, 1].set_title('Señal 5')
    plt.show()

  if (n == 6):
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(7, 10))
    ax[0, 0].plot(am_señaes[0])
    ax[0, 0].set_title('Señal 1')
    ax[0, 1].plot(am_señaes[1])
    ax[0, 1].set_title('Señal 2')
    ax[0, 2].plot(am_señaes[2])
    ax[0, 2].set_title("Señal 3")
    ax[1, 0].plot(am_señaes[3])
    ax[1, 0].set_title("Señal 4")
    ax[1, 1].plot(am_señaes[4])
    ax[1, 1].set_title('Señal 5')
    ax[1, 2].plot(am_señaes[5])
    ax[1, 2].set_title('Señal 6')
    plt.show()

  if (n == 7):
    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(7, 10))
    ax[0, 0].plot(am_señaes[0])
    ax[0, 0].set_title('Señal 1')
    ax[0, 1].plot(am_señaes[1])
    ax[0, 1].set_title('Señal 2')
    ax[0, 2].plot(am_señaes[2])
    ax[0, 2].set_title("Señal 3")
    ax[1, 0].plot(am_señaes[3])
    ax[1, 0].set_title("Señal 4")
    ax[1, 1].plot(am_señaes[4])
    ax[1, 1].set_title('Señal 5')
    ax[1, 2].plot(am_señaes[5])
    ax[1, 2].set_title('Señal 6')
    ax[2, 0].plot(am_señaes[6])
    ax[2, 0].set_title("Señal 7")
    plt.show()

  if (n == 8):
    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(7, 10))
    ax[0, 0].plot(am_señaes[0])
    ax[0, 0].set_title('Señal 1')
    ax[0, 1].plot(am_señaes[1])
    ax[0, 1].set_title('Señal 2')
    ax[0, 2].plot(am_señaes[2])
    ax[0, 2].set_title("Señal 3")
    ax[1, 0].plot(am_señaes[3])
    ax[1, 0].set_title("Señal 4")
    ax[1, 1].plot(am_señaes[4])
    ax[1, 1].set_title('Señal 5')
    ax[1, 2].plot(am_señaes[5])
    ax[1, 2].set_title('Señal 6')
    ax[2, 0].plot(am_señaes[6])
    ax[2, 0].set_title("Señal 7")
    ax[2, 1].plot(am_señaes[7])
    ax[2, 1].set_title("Señal 8")
    plt.show()

  if (n == 9):
    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(7, 10))
    ax[0, 0].plot(am_señaes[0])
    ax[0, 0].set_title('Señal 1')
    ax[0, 1].plot(am_señaes[1])
    ax[0, 1].set_title('Señal 2')
    ax[0, 2].plot(am_señaes[2])
    ax[0, 2].set_title("Señal 3")
    ax[1, 0].plot(am_señaes[3])
    ax[1, 0].set_title("Señal 4")
    ax[1, 1].plot(am_señaes[4])
    ax[1, 1].set_title('Señal 5')
    ax[1, 2].plot(am_señaes[5])
    ax[1, 2].set_title('Señal 6')
    ax[2, 0].plot(am_señaes[6])
    ax[2, 0].set_title("Señal 7")
    ax[2, 1].plot(am_señaes[7])
    ax[2, 1].set_title("Señal 8")
    ax[2, 2].plot(am_señaes[8])
    ax[2, 2].set_title('Señal 9')
    plt.show()

  if (n == 10):
    fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(7, 10))
    ax[0, 0].plot(am_señaes[0])
    ax[0, 0].set_title('Señal 1')
    ax[0, 1].plot(am_señaes[1])
    ax[0, 1].set_title('Señal 2')
    ax[0, 2].plot(am_señaes[2])
    ax[0, 2].set_title("Señal 3")
    ax[1, 0].plot(am_señaes[3])
    ax[1, 0].set_title("Señal 4")
    ax[1, 1].plot(am_señaes[4])
    ax[1, 1].set_title('Señal 5')
    ax[1, 2].plot(am_señaes[5])
    ax[1, 2].set_title('Señal 6')
    ax[2, 0].plot(am_señaes[6])
    ax[2, 0].set_title("Señal 7")
    ax[2, 1].plot(am_señaes[7])
    ax[2, 1].set_title("Señal 8")
    ax[2, 2].plot(am_señaes[8])
    ax[2, 2].set_title('Señal 9')
    ax[3, 0].plot(am_señaes[9])
    ax[3, 0].set_title('Señal 10')
    plt.show()

  if (n == 11):
    fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(7, 10))
    ax[0, 0].plot(am_señaes[0])
    ax[0, 0].set_title('Señal 1')
    ax[0, 1].plot(am_señaes[1])
    ax[0, 1].set_title('Señal 2')
    ax[0, 2].plot(am_señaes[2])
    ax[0, 2].set_title("Señal 3")
    ax[1, 0].plot(am_señaes[3])
    ax[1, 0].set_title("Señal 4")
    ax[1, 1].plot(am_señaes[4])
    ax[1, 1].set_title('Señal 5')
    ax[1, 2].plot(am_señaes[5])
    ax[1, 2].set_title('Señal 6')
    ax[2, 0].plot(am_señaes[6])
    ax[2, 0].set_title("Señal 7")
    ax[2, 1].plot(am_señaes[7])
    ax[2, 1].set_title("Señal 8")
    ax[2, 2].plot(am_señaes[8])
    ax[2, 2].set_title('Señal 9')
    ax[3, 0].plot(am_señaes[9])
    ax[3, 0].set_title('Señal 10')
    ax[3, 1].plot(am_señaes[10])
    ax[3, 1].set_title("Señal 11")
    plt.show()

  if (n == 12):
    fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(7, 10))
    ax[0, 0].plot(am_señaes[0])
    ax[0, 0].set_title('Señal 1')
    ax[0, 1].plot(am_señaes[1])
    ax[0, 1].set_title('Señal 2')
    ax[0, 2].plot(am_señaes[2])
    ax[0, 2].set_title("Señal 3")
    ax[1, 0].plot(am_señaes[3])
    ax[1, 0].set_title("Señal 4")
    ax[1, 1].plot(am_señaes[4])
    ax[1, 1].set_title('Señal 5')
    ax[1, 2].plot(am_señaes[5])
    ax[1, 2].set_title('Señal 6')
    ax[2, 0].plot(am_señaes[6])
    ax[2, 0].set_title("Señal 7")
    ax[2, 1].plot(am_señaes[7])
    ax[2, 1].set_title("Señal 8")
    ax[2, 2].plot(am_señaes[8])
    ax[2, 2].set_title('Señal 9')
    ax[3, 0].plot(am_señaes[9])
    ax[3, 0].set_title('Señal 10')
    ax[3, 1].plot(am_señaes[10])
    ax[3, 1].set_title("Señal 11")
    ax[3, 2].plot(am_señaes[11])
    ax[3, 2].set_title("Señal 12")
    plt.show()
   
    
  plt.figure(0)
  plt.plot(final);plt.title("Señal resultante")
  plt.show()
 
  yf = fft(final)
  xf = fftfreq(fs, 1/fs)[:fs//2]
  
  plt.stem(xf, 2.0/fs * np.abs(yf[0:fs//2]));plt.title("Densidad de potencia")
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

def TDM_Acc():
    ch = int(entry_tdma.get())
    data = []
    chanel1 = []
    chanel2 = []
    x1 = 0
    x_out = 0
    cont = 0
    frec = np.linspace(100, 400, ch)
    print(frec)
    fs = 10000
    Ts = 1/fs
    n = 0.15 / Ts
    n = np.arange(n)
    for i in frec:
        y = np.sin(2*np.pi*i*n*Ts)
        data.append(y)

    for i in range(0, 1000*ch):

        if i % 1000 == 1:
            x1 = not (x1)
            print(x_out)
            cont = 0
            x_out += 1
            if x_out == ch:
                x_out = 0
        x = data[x_out]
        if x1 == 1:
            chanel1.append(x[cont])
        else:
            chanel2.append(x[cont])
        cont += 1

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(chanel1)
    plt.title('canal 1')
    plt.subplot(2, 1, 2)
    plt.plot(chanel2)
    plt.title('canal 2')
    plt.show()
    #return (ch1)
  
  
  
#Interfaz menú
frame_0 = customtkinter.CTkFrame(master=menu)
frame_0.pack(pady=20, padx=40, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_0, text="Parcial Rescate", font=("Roboto Medium", -16) ,justify=tkinter.LEFT)
label_1.pack(pady=12, padx=10)

label_2 = customtkinter.CTkLabel(master=frame_0, text="Hecho por Andrés Corredor", font=("Roboto Medium", -12) ,justify=tkinter.LEFT)
label_2.place(x=75, y=70)
label_3 = customtkinter.CTkLabel(master=frame_0, text="Menu principal", font=("Roboto Medium", -12) ,justify=tkinter.LEFT)
label_3.place(x=108, y=90)

button_1 = customtkinter.CTkButton(master=frame_0, text="Cod. Línea", font=("Roboto Medium", -16) , command=linea)
button_1.place(x=75, y=125)

button_2 = customtkinter.CTkButton(master=frame_0, text="Cod. Canal", font=("Roboto Medium", -16) , command=canal)
button_2.place(x=75, y=155)

button_3 = customtkinter.CTkButton(master=frame_0, text="16 QAM", font=("Roboto Medium", -16) , command=qam_16)
button_3.place(x=75, y=185)

button_4 = customtkinter.CTkButton(master=frame_0, text="Mult - TDM", font=("Roboto Medium", -16) , command=fdm_acc)
button_4.place(x=75, y=215)

button_5 = customtkinter.CTkButton(master=frame_0, text="Acces - TDMA", font=("Roboto Medium", -16) , command=tdma)
button_5.place(x=75, y=245)



#interfaz codigo de linea
frame_1 = customtkinter.CTkFrame(master=app_linea)
frame_1.pack(pady=20, padx=40, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, text="Codificador de línea ", font=("Roboto Medium", -16) ,justify=tkinter.LEFT)
label_1.pack(pady=12, padx=10)

entry_bits_cl = customtkinter.CTkEntry(master=frame_1, placeholder_text="Numero de bits a codificar")
entry_bits_cl.place(x=75, y=58)

entry_roll_off = customtkinter.CTkEntry(master=frame_1, placeholder_text="Roll_off del filtro")
entry_roll_off.place(x=75, y = 90)


error_5 = customtkinter.CTkLabel(master=frame_1, text="", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
error_5.place(x=55, y=92)
button_1 = customtkinter.CTkButton(master=frame_1, text="Codificar", font=("Roboto Medium", -16) , command=Manchester)
button_1.place(x=75, y=120)

button_2 = customtkinter.CTkButton(master=frame_1, text="Cerrar", font=("Roboto Medium", -16) , command=app_linea.destroy)
button_2.place(x=75, y=150)


#Interfaz codigo canal
frame_3 = customtkinter.CTkFrame(master=app_canal)
frame_3.pack(pady=20, padx=40, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_3, text="Codificador Hamming ( 11, 7 )", font=("Roboto Medium", -16) ,justify=tkinter.LEFT)
label_1.pack(pady=12, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame_3, placeholder_text="binario de 7 bits")
entry_1.place(x=75, y=40)

error_1 = customtkinter.CTkLabel(master=frame_3, text="", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
error_1.place(x=55, y=60)

button_1 = customtkinter.CTkButton(master=frame_3, text="Codificar", font=("Roboto Medium", -16) , command=button_callback)
button_1.place(x=75, y=90)

label_2 = customtkinter.CTkLabel(master=frame_3, text="Mensaje codificado en Hamming:", font=("Roboto Medium", -12) ,justify=tkinter.LEFT)
label_2.place(x=55, y=120)

entry_2 = customtkinter.CTkEntry(master=frame_3, placeholder_text="Hamming de 11 bits")
entry_2.place(x=75, y=150)

error_2 = customtkinter.CTkLabel(master=frame_3, text="", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
error_2.place(x=35, y=180)

button_2 = customtkinter.CTkButton(master=frame_3, text="Generar Error", font=("Roboto Medium", -16) , command=button_gen_error)
button_2.place(x=75, y=210)

label_3 = customtkinter.CTkLabel(master=frame_3, text="Hamming con error:", font=("Roboto Medium", -12) ,justify=tkinter.LEFT)
label_3.place(x=55, y=240)

entry_3 = customtkinter.CTkEntry(master=frame_3, placeholder_text="Hamming con error")
entry_3.place(x=75, y=270)

error_3 = customtkinter.CTkLabel(master=frame_3, text="", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
error_3.place(x=35, y=300)

button_3 = customtkinter.CTkButton(master=frame_3, text="Corregir", font=("Roboto Medium", -16) , command=corrector)
button_3.place(x=75, y=330)

label_5 = customtkinter.CTkLabel(master=frame_3, text="Hamming corregido:", font=("Roboto Medium", -12) ,justify=tkinter.LEFT)
label_5.place(x=55, y=360)

entry_4 = customtkinter.CTkEntry(master=frame_3, placeholder_text="Hamming corregido")
entry_4.place(x=75, y=390)

label_6 = customtkinter.CTkLabel(master=frame_3, text="", font=("Roboto Medium", -12) ,justify=tkinter.LEFT)
label_6.place(x=10, y=420)

button_2 = customtkinter.CTkButton(master=frame_3, text="Cerrar", font=("Roboto Medium", -16) , command=app_canal.destroy)
button_2.place(x=75, y=450)



#Interfaz modulación 16 QAM

frame_4 = customtkinter.CTkFrame(master=app_mod_dig)
frame_4.pack(pady=20, padx=40, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_4, text="Modulador 16 QAM", font=("Roboto Medium", -16) ,justify=tkinter.LEFT)
label_1.pack(pady=12, padx=10)

entry_5 = customtkinter.CTkEntry(master=frame_4, placeholder_text="Numero de bits a modular")
entry_5.place(x=75, y=58)


error_5 = customtkinter.CTkLabel(master=frame_4, text="", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
error_5.place(x=55, y=92)
button_1 = customtkinter.CTkButton(master=frame_4, text="Modular", font=("Roboto Medium", -16) , command=button_dig)
button_1.place(x=75, y=110)
button_2 = customtkinter.CTkButton(master=frame_4, text="Cerrar", font=("Roboto Medium", -16) , command=app_mod_dig.destroy)
button_2.place(x=75, y=140)

#interfaz multiplexado
frame_5 = customtkinter.CTkFrame(master=app_mult)
frame_5.pack(pady=20, padx=40, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_5, text="Simulador de multiplexación FDM", font=("Roboto Medium", -16) ,justify=tkinter.LEFT)
label_1.pack(pady=12, padx=10)

entry_multi_canal = customtkinter.CTkEntry(master=frame_5, placeholder_text="Canales a codificar (0-12)")
entry_multi_canal.place(x=75, y=58)

error_6 = customtkinter.CTkLabel(master=frame_5, text="", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
error_6.place(x=55, y=92)
button_1 = customtkinter.CTkButton(master=frame_5, text="Simular", font=("Roboto Medium", -16) , command=FDM)
button_1.place(x=75, y=120)
button_2 = customtkinter.CTkButton(master=frame_5, text="Cerrar", font=("Roboto Medium", -16) , command=app_mult.destroy)
button_2.place(x=75, y=160)


#interfaz acceso multiple
frame_6 = customtkinter.CTkFrame(master=app_acc_mult)
frame_6.pack(pady=20, padx=40, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_6, text="Simulador de acceso multiple TDMA", font=("Roboto Medium", -16) ,justify=tkinter.LEFT)
label_1.pack(pady=12, padx=10)

entry_tdma = customtkinter.CTkEntry(master=frame_6, placeholder_text="número de canales")
entry_tdma.place(x=75, y=58)

error_6 = customtkinter.CTkLabel(master=frame_6, text="", font=("Roboto Medium", -9) ,justify=tkinter.LEFT)
error_6.place(x=55, y=92)
button_1 = customtkinter.CTkButton(master=frame_6, text="Simular", font=("Roboto Medium", -16) , command=TDM_Acc)
button_1.place(x=75, y=120)
button_2 = customtkinter.CTkButton(master=frame_6, text="Cerrar", font=("Roboto Medium", -16) , command=app_acc_mult.destroy)
button_2.place(x=75, y=160)

menu.mainloop()
