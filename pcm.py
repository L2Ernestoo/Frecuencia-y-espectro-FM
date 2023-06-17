# -*- coding: utf-8 -*-
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la captura de audio
CHUNK = 1024  # Tamaño del búfer de audio
FORMAT = pyaudio.paInt16  # Formato de los datos de audio
CHANNELS = 1  # Número de canales de audio (mono)
RATE = 44100  # Tasa de muestreo en Hz

# Inicializar PyAudio
p = pyaudio.PyAudio()

# Configuración del gráfico
fig, ax = plt.subplots()
x = np.arange(0, CHUNK)
line, = ax.plot(x, np.zeros(CHUNK))
ax.set_ylim(-32768, 32767)
ax.set_xlim(0, CHUNK)
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Espectro de Audio')


# Función de actualización del gráfico
def update_plot(data):
    line.set_ydata(data)
    fig.canvas.draw()
    fig.canvas.flush_events()


# Función de captura y procesamiento de audio
def audio_callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16)

    # Procesamiento PCM
    # Aquí puedes realizar el procesamiento PCM y calcular el espectro

    # Actualizar el gráfico en tiempo real
    update_plot(audio_data)

    return (in_data, pyaudio.paContinue)


# Configurar la captura de audio
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=audio_callback)

# Iniciar la captura de audio
stream.start_stream()

# Mantener la aplicación en ejecución hasta que se presione Ctrl+C
try:
    while True:
        plt.pause(0.1)
except KeyboardInterrupt:
    # Detener la captura de audio
    stream.stop_stream()
    stream.close()
    p.terminate()
