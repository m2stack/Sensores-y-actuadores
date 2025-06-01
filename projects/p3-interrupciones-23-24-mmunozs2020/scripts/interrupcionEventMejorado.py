#!/usr/bin/env python3
import signal
import sys
import time
import RPi.GPIO as GPIO

PIN_LED_V       = 19
PIN_LED_R       = 13

PIN_BOTON_V     = 21
PIN_BOTON_R     = 20


def callbackSalir(senial, cuadro): # señal y estado cuando se produjo la interrupcion.
    GPIO.cleanup () # limpieza de los recursos GPIO antes de salir
    sys.exit(0)

def callbackBotonVerde(canal):
    print("[INFO]: led verde encendido")
    pwm_v.start(100)
    time.sleep(0.25)
    pwm_v.stop()

def callbackBotonRojo (canal):
    print("[INFO]: led rojo encendido")
    pwm_r.start(100)
    time.sleep(0.25)
    pwm_r.stop()

def config_pin_led(pin):
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 100)
    return pwm 

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    # Activamos resistencia pull_up_down en modo HIGH, esto es:
    # - HIGH: estado por defecto del GPIO (no se ha pulsado).
    # - LOW: estado del GPIO cuando se ha pulsado el boton.
    GPIO.setup(PIN_BOTON_V, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_BOTON_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    pwm_v = config_pin_led(PIN_LED_V)
    pwm_r = config_pin_led(PIN_LED_R)
    
    # - control del botón que enciende el led verde:
    GPIO.add_event_detect(PIN_BOTON_V, GPIO.FALLING, 
      callback=callbackBotonVerde, bouncetime=500) # expresado en ms.
    
    # - control del botón que enciende el led rojo:
    GPIO.add_event_detect(PIN_BOTON_R, GPIO.FALLING, 
      callback=callbackBotonRojo, bouncetime=500) # expresado en ms.
    
    signal.signal(signal.SIGINT, callbackSalir) # callback para CTRL+C
    signal.pause() # esperamos por hilo/callback CTRL+C antes de acabar
