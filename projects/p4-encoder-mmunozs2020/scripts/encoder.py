#!/usr/bin/env python3
import signal
import sys
import time
import RPi.GPIO as GPIO
import threading

PIN_OPTO		= 18

ITS_POR_VUELTA	= 20 # la rueda tiene 20 muescas: 20 pasos = 1 vuelta

iteraciones 	= 0
ejecutando		= True

# funcion que establece los modos de los distintos pines como corresponde
def setup_inicial():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(PIN_OPTO, GPIO.IN)

def calculo_por_lectura():
	vueltas = iteraciones / ITS_POR_VUELTA
	rmp 	= 6 * vueltas # n vueltas en 60 seg dada la muestra de 10 seg
	
	# imprimimos la informacion de iteraciones, vueltas y rmp calculada
	print("--[INFO MOTOR]--------------")
	print("-[%.1f] iteraciones" % iteraciones)
	print("-[%.1f] vueltas / 10s" % vueltas)
	print("-[%.1f] rmp" % rmp)
	
	global ejecutando
	ejecutando = False
	return ejecutando
	
def callbackSalir(senial, cuadro): # señal y estado cuando se produjo la interrupcion.
    GPIO.cleanup () # limpieza de los recursos GPIO antes de salir
    sys.exit(0)

if __name__ == '__main__':
	
	setup_inicial()
	
	task_thread = threading.Timer(10, calculo_por_lectura)
	task_thread.start()
	
	while ejecutando:
		# en caso de detectar un cambio de 0 a 1, sumamos una iteracion (ha pasado una muesca)
		lectura = GPIO.wait_for_edge(PIN_OPTO, GPIO.RISING)
		if lectura: iteraciones += 1
