#!/usr/bin/env python3
import signal
import sys
import time
import RPi.GPIO as GPIO

PIN_PRESION     = 21
PIN_LED         = 26

ENCENDER        = 1
APAGAR          = 0
LIMITERACIONES  = 20


# funcion que establece los modos de los distintos pines como corresponde
def setup_inicial():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(PIN_PRESION, GPIO.IN)
    GPIO.setup(PIN_LED, GPIO.OUT)

# enciende el led con el numero de pin que recibe de parametro
# en caso de recibir 0 por su entrada, apaga el led
def encender_apagar_led(pin, on_off):
    if(on_off == ENCENDER): GPIO.output(pin, GPIO.HIGH)
    elif(on_off == APAGAR): GPIO.output(pin, GPIO.LOW)

# funcion para cuando la presion se detecta
def do_presion_detectada():
    encender_apagar_led(PIN_LED, ENCENDER)
    
# funcion para cuando la presion no se detecta
def do_presion_cero():
    encender_apagar_led(PIN_LED, APAGAR)

# -> funcion "master": control principal que actua según la presion 
def control_por_lectura(lectura, iteraciones):
    if(lectura == 1):
        if(iteraciones > 20):
            do_presion_detectada()
    elif(lectura == 0):
        do_presion_cero()
    
def callbackSalir(senial, cuadro): # señal y estado cuando se produjo la interrupcion.
    GPIO.cleanup() # limpieza de los recursos GPIO antes de salir
    sys.exit(0)
    
        
if __name__ == '__main__':
    
    setup_inicial()
    iteraciones = 0     # necesario por mal funcionamiento del sensor
    
    while True:
        lectura = GPIO.input(PIN_PRESION)
        if(lectura == 1):
            iteraciones += 1
        else:
            iteraciones = 0
            
        control_por_lectura(lectura, iteraciones)
        print("lectura = ", lectura)
                
        time.sleep(0.1)
        signal.signal(signal.SIGINT, callbackSalir) # callback para CTRL+C
