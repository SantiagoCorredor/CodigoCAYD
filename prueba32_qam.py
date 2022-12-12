import numpy as np
from scipy.special import erfc
from scipy import *
from random import randint
import matplotlib.pyplot as plt
import math

from commpy.modulation import PSKModem
from commpy.utilities import upsample

from sk_dsp_comm.digitalcom import sqrt_rc_imp, rc_imp, q_fctn
from sk_dsp_comm.sigsys import downsample, upsample, cpx_awgn

EbNo_min = 1e-4
EbNo_max = 0.5
M = 32
alpha = 0.3x
Ns = 1
Eb_No_dB = (np.arange(EbNo_min,EbNo_max + 1))
Eb_No_lin = (10**(Eb_No_dB/10.0))
    
 ## Se crea un objeto tipo psk
mod1 = PSKModem (M)
k = mod1.num_bits_symbol
    ##Se crearán variables vacías para ir añadiendo los valores
Pe = (np.empty(np.shape(Eb_No_lin)))
BER = (np.empty(np.shape(Eb_No_lin)))
    ## Parametros para el filtro
    
Ts = 1
Fs = 20
    ## Diseño del filtro
nsamp = (Fs*Ts)# Muestras por simbolo
filtro = (sqrt_rc_imp(nsamp,alpha))
    ##Creo los vectores de datos vinarios
x_tx = (np.random.randint(0,2,k*Ns))
    
    
m_tx = (mod1.modulate(x_tx))
    ##Sobre muestreo y filtro
y_tx = (upsample(m_tx,nsamp))
r_tx = (np.convolve(y_tx, filtro, mode = 'same'))
    ##Agrego ruido
for ebno in Eb_No_dB:
    error_sum = 0
    esno = (ebno + 10 * math.log(k,10))
    w = (cpx_awgn(r_tx, esno, nsamp))
      ##Sub muestreo y filtro
    y_rx = (np.convolve(w,filtro,mode = 'same'))
    m_rx = (downsample(y_rx,nsamp))
    x_rx = (mod1.modulate(m_rx))
    total_sent = (len(x_rx))
        
        ##Comparo la transmisión con los errores de recepción
    for u, v in zip (x_tx,x_rx):
         if u!=v:
             error_sum += 1
        ## Calculo el BER
    BER[loop] = (float(error_sum)/float(total_sent))
    loop += 1
loop = 0
for en in Eb_No_lin:
    Pe [loop] = ( (2/math.log(M,2)) * q_fctn(math.sqrt(2 * math.log(M,2) * en ) * math.sin(math.pi/M)))
    loop += 1
fig, ax = plt.subplots(3,1,sharex='col', figsize=(10, 14))
ax[0].plot(r_tx);ax[0].set_title('Clock')
ax[1].plot(y_tx);ax[1].set_title('Transmitidos')
ax[2].plot(y_rx); ax[2].set_title('Recibidos')
plt.show()