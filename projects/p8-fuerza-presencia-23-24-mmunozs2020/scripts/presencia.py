#!/usr/bin/env python3
import signal
import sys
import time
import RPi.GPIO as GPIO

PIN_LED         = 26
PIN_PRESENCIA   = 16

ENCENDER        = 1
APAGAR          = 0

# funcion que establece los modos de los distintos pines como corresponde
def setup_inicial():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(PIN_PRESENCIA, GPIO.IN)
    GPIO.setup(PIN_LED, GPIO.OUT)
    
    GPIO.add_event_detect(PIN_PRESENCIA, GPIO.BOTH) # (new)

# enciende el led con el numero de pin que recibe de parametro
# en caso de recibir 0 por su entrada, apaga el led
def encender_apagar_led(pin, on_off):
    if(on_off == ENCENDER): GPIO.output(pin, GPIO.HIGH)
    elif(on_off == APAGAR): GPIO.output(pin, GPIO.LOW)

# funcion para cuando hay presencia detectada
def do_presencia_detectada():
    encender_apagar_led(PIN_LED, ENCENDER)
    
# funcion para cuando no hay presencia
def do_presencia_cero():
    encender_apagar_led(PIN_LED, APAGAR)

# -> funcion "master": control principal que actua según la lectura de presencia 
def control_por_lectura(lectura):
    if(lectura == 1):
        do_presencia_detectada()
    elif(lectura == 0):
        do_presencia_cero()

def callbackSalir(senial, cuadro): # señal y estado cuando se produjo la interrupcion.
    GPIO.cleanup () # limpieza de los recursos GPIO antes de salir
    sys.exit(0)
    
        
if __name__ == '__main__':
    
    setup_inicial()
    
    while True:
        
        if GPIO.event_detected(PIN_PRESENCIA):
            lectura = GPIO.input(PIN_PRESENCIA)
            control_por_lectura(lectura)
                
        time.sleep(0.1)
        signal.signal(signal.SIGINT, callbackSalir) # callback para CTRL+C
