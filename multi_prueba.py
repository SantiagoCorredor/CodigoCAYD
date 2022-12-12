import pyaudio
import numpy as np
import threading
import matplotlib.pyplot as plt
from scipy.io import wavfile 


fs1, Audiodata1 = wavfile.read("grabacion.wav")
fs2, Audiodata2 = wavfile.read("grabacion1.wav")
fs3, Audiodata3 = wavfile.read("grabacion2.wav")


AudiodataScaled1 = Audiodata1/(2**15)
print(len(AudiodataScaled1))

#definir los valores del eje x en milisegundos
timeValues1 = np.arange(0, len(AudiodataScaled1), 1)/ fs1 # Convertir Muestras/Seg a Segundos
#timeValues = timeValues * 1000  #Escala de tiempo en milisegundos
print(timeValues1[len(timeValues1)-1])
timeValues1.flatten().tolist()
while(timeValues1[len(timeValues1)-1] < 10):
    aumento = timeValues1[1]-timeValues1[0]
    aux = timeValues1[len(timeValues1)-1] + aumento
    timeValues1.append(aux)
    print(len(timeValues1))

    
print(timeValues1[len(timeValues1)-1])
print(timeValues1[len(timeValues1)-2])
AudiodataScaled2 = Audiodata2/(2**15)


#definir los valores del eje x en milisegundos
timeValues2 = np.arange(0, len(AudiodataScaled2), 1)/ fs2 # Convertir Muestras/Seg a Segundos
#timeValues = timeValues * 1000  #Escala de tiempo en milisegundos

AudiodataScaled3 = Audiodata3/(2**15)

#definir los valores del eje x en milisegundos
timeValues3 = np.arange(0, len(AudiodataScaled3), 1)/ f3 # Convertir Muestras/Seg a Segundos
#timeValues = timeValues * 1000  #Escala de tiempo en milisegundos




plt.plot(timeValues, AudiodataScaledT);plt.title('Señal de Audio Con Informacion de Ejes',size=16)
plt.text(0-100, np.max(AudiodataScaledT), 'Máximo', fontsize = 16,bbox=dict(facecolor='red', alpha=0.5))
plt.ylabel('Amplitud'); plt.xlabel('Tiempo (ms)');
plt.show()