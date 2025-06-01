#!/usr/bin/python
import RPi.GPIO as GPIO
import time

PIN_ROJO          = 26
PIN_AMARILLO      = 19
PIN_VERDE         = 13

PIN_TRIGGER       = 21
PIN_ECHO          = 20

distancia_peligro = 0
distancia_cautela = 0


def es_entero(i):
      try:
            int(i)
            return True
      except ValueError:
            return False

def leer_distancia():
      GPIO.output(PIN_TRIGGER, GPIO.HIGH)
      time.sleep(0.00001)
      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      while GPIO.input(PIN_ECHO)==0:
            inicioPulso = time.time()
      while GPIO.input(PIN_ECHO)==1:
            finPulso = time.time()

      duracionPulso = finPulso - inicioPulso
      distancia = round(duracionPulso * 17150, 2)
      
      return distancia

def encender_1_led(pin):
      for i in (PIN_ROJO, PIN_AMARILLO, PIN_VERDE):
            if(i == pin): GPIO.output(i, GPIO.HIGH)
            else: GPIO.output(i, GPIO.LOW)

def control_led(dist):
      if(dist < distancia_peligro):
            encender_1_led(PIN_ROJO)
      elif(dist < distancia_cautela):
            encender_1_led(PIN_AMARILLO)
      else:
            encender_1_led(PIN_VERDE)
      

ds = input("Establece una distancia de seguridad (en cm): ")
while(not es_entero(ds)):
      ds = input("Por favor, introduce un valor entero: ")
distancia_peligro = float(ds)
distancia_cautela = float(distancia_peligro * 2)

try:
      GPIO.setmode(GPIO.BCM)

      GPIO.setup(PIN_TRIGGER, GPIO.OUT)
      GPIO.setup(PIN_ECHO, GPIO.IN)
      GPIO.setup(PIN_ROJO, GPIO.OUT)
      GPIO.setup(PIN_AMARILLO, GPIO.OUT)
      GPIO.setup(PIN_VERDE, GPIO.OUT)
      
      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      print("Esperando a que se estabilice el US")
      time.sleep(2)
      
      while True:
            distancia_medida = leer_distancia()
            control_led(distancia_medida)
            print("Distancia: ", distancia_medida, " cm")
            
            time.sleep(0.5)
      
except KeyboardInterrupt:
      print("Terminando programa...")
      GPIO.cleanup()
      
      
