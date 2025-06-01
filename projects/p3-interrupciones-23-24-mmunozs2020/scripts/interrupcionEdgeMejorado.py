#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

PIN_LED_V       = 19
PIN_LED_R       = 13

PIN_BOTON_V     = 21
PIN_BOTON_R     = 20


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

    while True:

        # - control del botón que enciende el led verde:
        if not GPIO.input(PIN_BOTON_V):
            pwm_v.start(100)
            print("[INFO]: led verde encendido")
            GPIO.wait_for_edge(PIN_BOTON_V, GPIO.RISING)
            pwm_v.stop()

        # - control del botón que enciende el led rojo:
        if not GPIO.input(PIN_BOTON_R):
            pwm_r.start(100)
            print("[INFO]: led rojo encendido")
            GPIO.wait_for_edge(PIN_BOTON_R, GPIO.RISING)
            pwm_r.stop()

        # print("<LOOP>") # - traza únicamente para pruebas adicionales
        
 
	
