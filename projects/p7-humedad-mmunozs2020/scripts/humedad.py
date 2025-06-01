#!/usr/bin/env python3
import signal
import sys
import time
import RPi.GPIO as GPIO

PIN_LED_V       = 16
PIN_LED_A       = 20
PIN_LED_R       = 21

PIN_ZUMBADOR    = 26

PIN_HUMEDAD     = 23

# estados por los que pasa el programa en humedad baja segun el tiempo
VERDE       = 3
AMARILLO    = 2
ROJO        = 1
GRITOS      = 0

s           = VERDE
c           = 50


# funcion que establece los modos de los distintos pines como corresponde
def setup_inicial():
    GPIO.setmode(GPIO.BCM)
    
    for i in (PIN_LED_V, PIN_LED_A, PIN_LED_R, PIN_ZUMBADOR):
        GPIO.setup(i, GPIO.OUT)
    GPIO.setup(PIN_HUMEDAD, GPIO.IN)

# enciende el led con el numero de pin que recibe de parametro
def encender_1_led(pin):
      for i in (PIN_LED_V, PIN_LED_A, PIN_LED_R):
            if(i == pin): GPIO.output(i, GPIO.HIGH)
            else: GPIO.output(i, GPIO.LOW)

# funcion para cuando la humedad es la suficiente (alta)
def do_humedad_alta(counter, status):
    encender_1_led(PIN_LED_V)
    counter = 50
    status = VERDE
    return counter, status
    
# funcion para cuando la humedad es demasiado baja
def do_humedad_baja(counter, status):
    if counter == 50:
        print("Me estoy deshidratando")
    if counter > 0:
        counter -= 1
    else:
        status = cambiar_temperamento(status)
        counter = 50
    return counter, status

# actualiza los comportamientos según va cambiando el estado (s)
def cambiar_temperamento(status):
    if(status > GRITOS): status -= 1
    if(status == AMARILLO): encender_1_led(PIN_LED_A)
    if(status == ROJO): encender_1_led(PIN_LED_R)
    
    return status

# -> funcion "master": control principal que actua según la humedad
def control_por_lectura(lectura, counter, status):
    if(lectura == 0):
        counter, status = do_humedad_alta(counter, status)
    elif(lectura == 1):
        counter, status = do_humedad_baja(counter, status)
    return counter, status
    

def callbackSalir(senial, cuadro): # señal y estado cuando se produjo la interrupcion.
    GPIO.cleanup () # limpieza de los recursos GPIO antes de salir
    sys.exit(0)


if __name__ == '__main__':
    setup_inicial()
    
    pwm = GPIO.PWM(PIN_ZUMBADOR, 1000)
    pwm.start(0)
    
    encender_1_led(PIN_LED_V)
    
    while True:
        lectura = GPIO.input(PIN_HUMEDAD)
        
        c, s = control_por_lectura(lectura, c, s)
        if(s == GRITOS):
            pwm.ChangeDutyCycle(100) 
            time.sleep(0.1)
            pwm.ChangeDutyCycle(0)
            print("ME DESHIDRATOOOO AAAAAAAAAAAAAAAAAHHHHH!!!")
        
        time.sleep(0.1)
        signal.signal(signal.SIGINT, callbackSalir) # callback para CTRL+C
        # signal.pause() # esperamos por hilo/callback CTRL+C antes de acabar
    
    
