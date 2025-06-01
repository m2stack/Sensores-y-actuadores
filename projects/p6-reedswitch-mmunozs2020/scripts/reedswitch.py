#!/usr/bin/env python3
import signal
import sys
import time
import RPi.GPIO as GPIO
import threading

PIN_REEDSWITCH	= 12
PIN_LED			= 26

ENCENDER        = 1
APAGAR          = 0


# funcion que establece los modos de los distintos pines como corresponde
def setup_inicial():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(PIN_REEDSWITCH, GPIO.IN)
    GPIO.setup(PIN_LED, GPIO.OUT)

# enciende el led con el numero de pin que recibe de parametro
# en caso de recibir 0 por su entrada, apaga el led
def encender_apagar_led(pin, on_off):
    if(on_off == ENCENDER): GPIO.output(pin, GPIO.HIGH)
    elif(on_off == APAGAR): GPIO.output(pin, GPIO.LOW)

# controla el estado del led según la lectura recibida y el numero de iteraciones
def control_por_lectura(lectura, iteraciones):
	if not lectura:
		if iteraciones < 15:
			iteraciones += 1
		else:
			encender_apagar_led(PIN_LED, ENCENDER)
	else:
		iteraciones = 0
		encender_apagar_led(PIN_LED, APAGAR)
		
	return iteraciones
		
def callbackSalir(senial, cuadro): # señal y estado cuando se produjo la interrupcion.
    GPIO.cleanup() # limpieza de los recursos GPIO antes de salir
    sys.exit(0)

if __name__ == '__main__':
	
	setup_inicial()
	iteraciones = 0
	
	while True:
		lectura = GPIO.input(PIN_REEDSWITCH)
		
		iteraciones = control_por_lectura(lectura, iteraciones)
		signal.signal(signal.SIGINT, callbackSalir) # callback para CTRL+C
		
		time.sleep(0.05)
