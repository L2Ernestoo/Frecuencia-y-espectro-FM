# -*- coding: utf-8 -*-

import serial
import matplotlib.pyplot as plt

# ConfiguraciÃ³n del puerto serial
serial_port = '/dev/tty.usbmodem11101'  # Reemplaza por el puerto correcto
baud_rate = 9600

# ConfiguraciÃ³n del grÃ¡fico
plt.ion()  # Modo interactivo para actualizaciÃ³n en tiempo real
fig, ax = plt.subplots()
x = []  # Lista para almacenar los valores de tiempo
y = []  # Lista para almacenar los valores de frecuencia
line, = ax.plot(x, y)
ax.set_xlabel('Tiempo')
ax.set_ylabel('Frecuencia')

# ConfiguraciÃ³n del puerto serial
arduino = serial.Serial(serial_port, baud_rate, timeout=1)

# Lectura y visualizaciÃ³n en tiempo real
while True:
    # Lectura de los datos del Arduino
    data = arduino.readline().decode().strip()
    if data.startswith("frecuencia: "):
        freq_str = data.split(":")[1].strip()
        try:
            frecuencia = float(freq_str)
            print('Frecuencia:', frecuencia)

            # Agregar los valores a las listas
            x.append(len(x) + 1)
            y.append(frecuencia)

            # Actualizar el grÃ¡fico en tiempo real
            line.set_data(x, y)
            ax.relim()
            ax.autoscale_view()

            # Actualizar el título del gráfico con la frecuencia
            ax.set_title('Espectro de Frecuencia (Frecuencia: {:.2f} MHz)'.format(frecuencia))

            # Actualizar la visualizaciÃ³n
            plt.draw()
            plt.pause(0.01)
        except ValueError:
            print("Formato de frecuencia incorrecto:", freq_str)
    else:
        print("Datos no vÃ¡lidos:", data)
