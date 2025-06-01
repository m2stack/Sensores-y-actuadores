#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

PIN_LED_V       = 19
PIN_LED_R       = 13

PIN_BOTON_V     = 21
PIN_BOTON_R     = 20

v_pulsado       = False
r_pulsado       = False


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
        # en caso de detectar una pulsación (comprobada doblemente con 
        # según qué variable global v_pulsado o r_pulsado) encendemos
        # el led durante 1/4 de segundo y seguidamente lo apagamos
        
        # - control del botón que enciende el led verde:
        if (not GPIO.input(PIN_BOTON_V)) and (not v_pulsado):
            v_pulsado = True
            pwm_v.start(100)
            print("[INFO]: led verde encendido")
            time.sleep(0.25)
            pwm_v.stop()
        else:
            # si el botón se ha dejado de pulsar, actualizamos la
            # variable de doble comprobación (en este caso v_pulsado)
            if not GPIO.input(PIN_BOTON_V): v_pulsado = False
            
        # - control del botón que enciende el led rojo:
        if (not GPIO.input(PIN_BOTON_R)) and (not r_pulsado):
            r_pulsado = True
            pwm_r.start(100)
            print("[INFO]: led rojo encendido")
            time.sleep(0.25)
            pwm_r.stop()
        else:
            if not GPIO.input(PIN_BOTON_R): r_pulsado = False

        time.sleep(0.1)
        # print("<LOOP>") # - traza únicamente para pruebas adicionales


# [ NOTA: ]
# en la ejecución, al haber un sleep entre encendido y apagado de CADA 
# led, no vemos que se enciendan a la vez en ningún momento pese a tener
# controles separados el uno del otro. Sin embargo, si nos fijamos se
# puede apreciar que al pulsar ambos botones un corto plazo (1/3 de 
# segundo), se encienden y apagan secuencialmente en una misma pasada
# del bucle (más visible al descomentar la última traza)
