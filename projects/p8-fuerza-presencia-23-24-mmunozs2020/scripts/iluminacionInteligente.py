#!/usr/bin/env python3
import signal
import sys
import time
import RPi.GPIO as GPIO

PIN_PRESENCIA   = 16
PIN_PRESION     = 21
PIN_LED         = 26

ENCENDER        = 1
APAGAR          = 0
LIMITERACIONES  = 20


# funcion que establece los modos de los distintos pines como corresponde
def setup_inicial():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(PIN_PRESENCIA, GPIO.IN)
    GPIO.setup(PIN_PRESION, GPIO.IN)
    GPIO.setup(PIN_LED, GPIO.OUT)
    
    GPIO.add_event_detect(PIN_PRESENCIA, GPIO.BOTH)

# enciende el led con el numero de pin que recibe de parametro
# en caso de recibir 0 por su entrada, apaga el led
def encender_apagar_led(pin, on_off):
    if(on_off == ENCENDER): GPIO.output(pin, GPIO.HIGH)
    elif(on_off == APAGAR): GPIO.output(pin, GPIO.LOW)

# controla cuando se detecta como activo el sensor de presion
# con una comprobacion doble por iteraciones dado su mal funcionamiento
def control_presion(iteraciones):
    presion_detectada = False
    
    if(GPIO.input(PIN_PRESION) == 1):
        if(iteraciones < 20):
            iteraciones += 1
        else:
            presion_detectada = True
    else:
        iteraciones = 0
    
    return presion_detectada, iteraciones

# en caso de detectar presencia, establece un temporizador para encender
# el led 10 segundos tras haberse detectado
def control_presencia(accion_led, timer_led):
    if(GPIO.event_detected(PIN_PRESENCIA) and GPIO.input(PIN_PRESENCIA) == 1):
        accion_led = ENCENDER
        timer_led = time.time() + 10
        
    return accion_led, timer_led

# enciende o apaga el led segun los parametros de accion y timer recibidos
def control_led(accion_led, timer_led):
    if(accion_led == ENCENDER and timer_led >= time.time()):
        encender_apagar_led(PIN_LED, ENCENDER)
    else:
        encender_apagar_led(PIN_LED, APAGAR)

def callbackSalir(senial, cuadro): # señal y estado cuando se produjo la interrupcion.
    GPIO.cleanup () # limpieza de los recursos GPIO antes de salir
    sys.exit(0)
    
        
if __name__ == '__main__':
    
    setup_inicial()
    
    presion_detectada   = False
    iters_presion       = 0
    
    timer_presencia     = 0
    timer_led           = 0
    accion_led          = APAGAR
    
    ctime               = 0
    
    while True:
        ctime = time.time()
        # si detectamos presion, activamos la deteccion de presencia por
        # 30 segundos desde que ha sido pulsado
        presion_detectada, iters_presion = control_presion(iters_presion)
        if presion_detectada:
            timer_presencia = ctime + 30
        
        # si la deteccion de presencia está activa por tiempo, se
        # establecen los valores de accion y timer led que correspondan
        if timer_presencia >= ctime:
            accion_led, timer_led = control_presencia(accion_led, timer_led)
        
        # segun los valores de accion y timer led, se enciende o apaga
        # este mismo
        control_led(accion_led, timer_led)
        
        # print("---- INFO[%.1f] -------------" % ctime)
        # print("- presion_detectada: ", presion_detectada)
        # print("- iters_presion:     ", iters_presion)
        # print("- timer_presencia:   ", timer_presencia)
        # print("-----------------------------")
        # print(" ")
        
        time.sleep(0.1)
        signal.signal(signal.SIGINT, callbackSalir) # callback para CTRL+C
        
